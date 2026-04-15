import csv
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django_q.tasks import async_task
from moas.models import MOARequest
from applications.models import InternshipApplication, ApplicationMessage
from evaluations.models import InternshipEvaluation
from notifications.models import Notification
from reviews.models import CompanyReview
from .utils import generate_endorsement_pdf

def is_admin(user):
    return user.is_active and (user.is_staff or user.is_superuser)

@user_passes_test(is_admin)
def dashboard(request):
    pending_moas = MOARequest.objects.filter(status='pending').count()
    active_applications = InternshipApplication.objects.exclude(status__in=['draft', 'rejected']).count()
    
    # --- Analytics Data ---
    # MOA status distribution for Pie Chart
    moa_status_data = list(
        MOARequest.objects.values('status').annotate(count=Count('id')).order_by('status')
    )
    moa_labels = [dict(MOARequest.STATUS_CHOICES).get(item['status'], item['status']) for item in moa_status_data]
    moa_counts = [item['count'] for item in moa_status_data]
    
    # Top 5 companies by application count for Bar Chart
    top_companies_data = list(
        InternshipApplication.objects.values('company__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    company_labels = [item['company__name'] for item in top_companies_data]
    company_counts = [item['count'] for item in top_companies_data]

    # Application status distribution for Doughnut Chart
    app_status_data = list(
        InternshipApplication.objects.values('status').annotate(count=Count('id')).order_by('status')
    )
    app_labels = [dict(InternshipApplication.STATUS_CHOICES).get(item['status'], item['status']) for item in app_status_data]
    app_counts = [item['count'] for item in app_status_data]
    
    context = {
        'pending_moas': pending_moas,
        'active_applications': active_applications,
        # JSON-safe data for Chart.js
        'moa_labels': json.dumps(moa_labels),
        'moa_counts': json.dumps(moa_counts),
        'company_labels': json.dumps(company_labels),
        'company_counts': json.dumps(company_counts),
        'app_labels': json.dumps(app_labels),
        'app_counts': json.dumps(app_counts),
    }
    return render(request, 'university_admin/dashboard.html', context)

@user_passes_test(is_admin)
def moa_requests_list(request):
    moa_requests = MOARequest.objects.all().order_by('-date_requested')
    return render(request, 'university_admin/moa_list.html', {'moa_requests': moa_requests})

@user_passes_test(is_admin)
def manage_moa_request(request, pk):
    moa_request = get_object_or_404(MOARequest, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != moa_request.status:
            moa_request.status = new_status
            moa_request.save()

            # Create notification for the student
            Notification.objects.create(
                user=moa_request.student,
                title=f"MOA Request Updated: {moa_request.target_company_name}",
                message=f"Your MOA request status has been changed to: {moa_request.get_status_display()}.",
                link=f"/moas/my-requests/"
            )

            # Dispatch email asynchronously via django-q2 background worker
            async_task('moas.tasks.send_moa_status_email', moa_request.pk)
            
            messages.success(request, f"MOA Request status updated to {moa_request.get_status_display()}. Notification and email queued.")
            return redirect('university_admin:moa_list')
            
    return render(request, 'university_admin/manage_moa.html', {'moa_request': moa_request, 'status_choices': MOARequest.STATUS_CHOICES})

@user_passes_test(is_admin)
def applications_list(request):
    applications = InternshipApplication.objects.all().order_by('-application_date')
    return render(request, 'university_admin/app_list.html', {'applications': applications})

@user_passes_test(is_admin)
def manage_application(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_message = request.POST.get('message_content')
        
        if new_message:
            ApplicationMessage.objects.create(
                application=application,
                sender=request.user,
                content=new_message,
                is_from_admin=True
            )
            # Notify the student about the new message
            Notification.objects.create(
                user=application.student,
                title=f"New message on your {application.company.name} application",
                message=f"An administrator sent you a message regarding your internship application.",
                link=f"/applications/{application.pk}/"
            )
            messages.success(request, 'Message added to the thread.')
            return redirect('university_admin:manage_app', pk=pk)
            
        elif new_status and new_status != application.status:
            application.status = new_status
            application.save()
            
            # Dispatch email asynchronously via django-q2 background worker
            async_task('applications.tasks.send_status_email', application.pk)
            
            # Create notification for the student
            Notification.objects.create(
                user=application.student,
                title=f"Application Updated: {application.company.name}",
                message=f"Your application status has been changed to: {application.get_status_display()}.",
                link=f"/applications/{application.pk}/"
            )
            
            messages.success(request, f"Application status updated to {application.get_status_display()}. Email notification queued.")
            return redirect('university_admin:app_list')
            
    thread_messages = application.messages.all().order_by('created_at')
            
    return render(request, 'university_admin/manage_app.html', {
        'application': application, 
        'status_choices': InternshipApplication.STATUS_CHOICES,
        'thread_messages': thread_messages
    })

from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import User, Group

# --- Application Views (existing) ---

@user_passes_test(is_admin)
@permission_required('university_admin.can_generate_endorsement', raise_exception=True)
def download_endorsement_letter(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Endorsement_{application.student.username}_{application.company.name}.pdf"'
    
    generate_endorsement_pdf(application, response)
    
    return response

@user_passes_test(is_admin)
@permission_required('university_admin.can_export_data', raise_exception=True)
def export_moas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="moas_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Student', 'Target Company', 'Contact Person', 'Email', 'Status', 'Date Requested'])
    
    moas = MOARequest.objects.all().order_by('-date_requested')
    for moa in moas:
        writer.writerow([
            moa.id,
            moa.student.username,
            moa.target_company_name,
            moa.company_contact_person,
            moa.company_contact_email,
            moa.get_status_display(),
            moa.date_requested.strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    return response

@user_passes_test(is_admin)
@permission_required('university_admin.can_export_data', raise_exception=True)
def export_applications_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Student', 'Company', 'Status', 'Date Applied'])
    
    apps = InternshipApplication.objects.all().order_by('-application_date')
    for app in apps:
        writer.writerow([
            app.id,
            app.student.username,
            app.company.name,
            app.get_status_display(),
            app.application_date.strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    return response

# --- Role Management Views ---

@user_passes_test(is_admin)
@permission_required('university_admin.can_manage_roles', raise_exception=True)
def manage_roles(request):
    """View to list all staff users and their current roles."""
    staff_users = User.objects.filter(is_staff=True).exclude(is_superuser=True).prefetch_related('groups')
    return render(request, 'university_admin/manage_roles.html', {'staff_users': staff_users})

@user_passes_test(is_admin)
@permission_required('university_admin.can_manage_roles', raise_exception=True)
def edit_user_role(request, user_id):
    """Update a staff user's assigned group (Role)."""
    target_user = get_object_or_404(User, id=user_id, is_staff=True)
    if target_user.is_superuser:
        messages.error(request, "Superuser roles cannot be modified through this portal.")
        return redirect('university_admin:manage_roles')

    groups = Group.objects.all()

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        if group_id:
            try:
                new_group = Group.objects.get(id=group_id)
                target_user.groups.clear()
                target_user.groups.add(new_group)
                messages.success(request, f"Role for {target_user.username} updated to {new_group.name}.")
            except Group.DoesNotExist:
                messages.error(request, "Selected role does not exist.")
        else:
            target_user.groups.clear()
            messages.success(request, f"Removed all roles from {target_user.username}.")
        
        return redirect('university_admin:manage_roles')

    return render(request, 'university_admin/edit_user_role.html', {
        'target_user': target_user,
        'groups': groups
    })

@user_passes_test(is_admin)
def evaluations_list(request):
    """List all submitted evaluations with review status badges."""
    evaluations = InternshipEvaluation.objects.select_related(
        'application__student', 'application__company', 'evaluator'
    ).all().order_by('-created_at')
    return render(request, 'university_admin/eval_list.html', {'evaluations': evaluations})

@user_passes_test(is_admin)
def evaluation_detail(request, pk):
    """View full evaluation detail and approve it (making it visible to the student)."""
    evaluation = get_object_or_404(
        InternshipEvaluation.objects.select_related(
            'application__student', 'application__company', 'evaluator'
        ),
        pk=pk
    )

    if request.method == 'POST' and 'approve' in request.POST:
        if evaluation.review_status != 'approved':
            evaluation.review_status = 'approved'
            evaluation.save()

            # Now notify the student that their evaluation is ready to view
            Notification.objects.create(
                user=evaluation.application.student,
                title=f"Internship Evaluation Available: {evaluation.application.company.name}",
                message=f"Your internship evaluation has been reviewed and approved. You can now view your performance results.",
                link=f"/applications/{evaluation.application.pk}/"
            )

            messages.success(request, "Evaluation approved! The student has been notified and can now view their results.")
        else:
            messages.info(request, "This evaluation has already been approved.")
        return redirect('university_admin:evaluation_detail', pk=pk)

    return render(request, 'university_admin/eval_detail.html', {'evaluation': evaluation})

# --- Review Management Views ---

@user_passes_test(is_admin)
def reviews_list(request):
    """List all reviews, prioritizing pending reviews at the top."""
    filtered_reviews = CompanyReview.objects.select_related('student', 'company').all().order_by(
        'status', '-created_at' # 'approved' string is before 'pending_review', wait we want pending first. 
    )
    # the choices are 'approved' and 'pending_review' 
    # to order by pending first we can just order by '-status' since 'p' > 'a'
    filtered_reviews = CompanyReview.objects.select_related('student', 'company').all().order_by(
        '-status', '-created_at'
    )
    
    return render(request, 'university_admin/review_list.html', {'reviews': filtered_reviews})

@user_passes_test(is_admin)
def review_detail(request, pk):
    """View flagged review details and approve/delete them."""
    review = get_object_or_404(CompanyReview.objects.select_related('student', 'company'), pk=pk)

    if request.method == 'POST':
        if 'approve' in request.POST:
            review.status = 'approved'
            review.save()
            messages.success(request, "Review has been approved and is now public.")
            return redirect('university_admin:reviews_list')
            
        elif 'delete' in request.POST:
            review.delete()
            messages.success(request, "Review has been deleted.")
            return redirect('university_admin:reviews_list')

    return render(request, 'university_admin/review_detail.html', {'review': review})

