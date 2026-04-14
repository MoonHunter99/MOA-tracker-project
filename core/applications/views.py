from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InternshipApplication, ApplicationMessage
from .forms import ApplicationForm
from companies.models import Company
from django.contrib.auth.models import User
from notifications.models import Notification
# Create your views here.

@login_required 
def apply_to_company(request, company_id):
    company = get_object_or_404(Company, id=company_id, is_active=True)
    
    # Optional: Prevent the student from applying twice
    if InternshipApplication.objects.filter(student=request.user, company=company).exists():
        return redirect('companies:company_detail', pk=company.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.company = company
            application.status = 'submitted'
            application.save()

            # Notify all admin/staff users about the new application
            admin_users = User.objects.filter(is_staff=True)
            for admin_user in admin_users:
                Notification.objects.create(
                    user=admin_user,
                    title=f"New Application: {request.user.username}",
                    message=f"{request.user.username} applied to {company.name}.",
                    link=f"/dashboard/admin/applications/{application.pk}/"
                )
            return redirect('applications:my_applications') # Redirect to the new dashboard after applying
    else:
        form = ApplicationForm()

    context = {
        'form': form,
        'company': company,
    }
    return render(request, 'applications/apply.html', context)

@login_required
def my_applications(request):
    # Fetch all applications for the logged-in user, ordered by newest first
    applications = InternshipApplication.objects.filter(student=request.user).order_by('-application_date')
    
    context = {
        'applications': applications,
    }
    return render(request, 'applications/my_applications.html', context)

@login_required
def application_detail(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk, student=request.user)
    
    if request.method == 'POST':
        new_message = request.POST.get('message_content')
        if new_message:
            ApplicationMessage.objects.create(
                application=application,
                sender=request.user,
                content=new_message,
                is_from_admin=False
            )
            # Notify all admin/staff users about the new student message
            admin_users = User.objects.filter(is_staff=True)
            for admin_user in admin_users:
                Notification.objects.create(
                    user=admin_user,
                    title=f"New message from {request.user.username}",
                    message=f"{request.user.username} sent a message on their {application.company.name} application.",
                    link=f"/dashboard/admin/applications/{application.pk}/"
                )
            return redirect('applications:application_detail', pk=pk)
            
    thread_messages = application.messages.all().order_by('created_at')

    # Only show evaluation to students if admin has approved it
    evaluation = getattr(application, 'evaluation', None)
    if evaluation and evaluation.review_status != 'approved':
        evaluation = None
    
    context = {
        'application': application,
        'thread_messages': thread_messages,
        'evaluation': evaluation,
    }
    return render(request, 'applications/application_detail.html', context)