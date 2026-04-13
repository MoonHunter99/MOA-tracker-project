import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from moas.models import MOARequest
from applications.models import InternshipApplication
from .utils import generate_endorsement_pdf

def is_admin(user):
    return user.is_active and (user.is_staff or user.is_superuser)

@user_passes_test(is_admin)
def dashboard(request):
    pending_moas = MOARequest.objects.filter(status='pending').count()
    active_applications = InternshipApplication.objects.exclude(status__in=['draft', 'rejected']).count()
    
    context = {
        'pending_moas': pending_moas,
        'active_applications': active_applications,
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
            
            # Phase 3: Trigger Email Notification
            subject = f"Update: Your MOA Request for {moa_request.target_company_name}"
            message = f"Hello {moa_request.student.username},\n\nYour MOA Request for {moa_request.target_company_name} has been updated to: {moa_request.get_status_display()}.\n\nThank you,\nPUP Admin Team"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [moa_request.student.email],
                fail_silently=True,
            )
            messages.success(request, f"MOA Request status updated to {moa_request.get_status_display()} and email sent via console.")
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
        if new_status and new_status != application.status:
            application.status = new_status
            application.save()
            
            # Phase 3: Trigger Email Notification
            subject = f"Update: Your Internship Application for {application.company.name}"
            message = f"Hello {application.student.username},\n\nYour application status for {application.company.name} has been updated to: {application.get_status_display()}.\n\nThank you,\nPUP Admin Team"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [application.student.email],
                fail_silently=True,
            )
            messages.success(request, f"Application status updated to {application.get_status_display()} and email sent via console.")
            return redirect('university_admin:app_list')
            
    return render(request, 'university_admin/manage_app.html', {'application': application, 'status_choices': InternshipApplication.STATUS_CHOICES})

@user_passes_test(is_admin)
def download_endorsement_letter(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Endorsement_{application.student.username}_{application.company.name}.pdf"'
    
    generate_endorsement_pdf(application, response)
    
    return response

@user_passes_test(is_admin)
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
