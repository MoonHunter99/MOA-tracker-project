from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from companies.models import Company
from applications.models import InternshipApplication, ApplicationMessage
from evaluations.models import InternshipEvaluation
from evaluations.forms import EvaluationForm
from notifications.models import Notification

def is_company_partner(user):
    return hasattr(user, 'companyprofile')

@login_required
@user_passes_test(is_company_partner, login_url='/accounts/login/')
def portal_dashboard(request):
    company = request.user.companyprofile.company
    applications = InternshipApplication.objects.filter(company=company).order_by('-application_date')
    
    context = {
        'company': company,
        'applications': applications
    }
    return render(request, 'companies/portal/dashboard.html', context)

@login_required
@user_passes_test(is_company_partner, login_url='/accounts/login/')
def portal_app_detail(request, pk):
    company = request.user.companyprofile.company
    application = get_object_or_404(InternshipApplication, pk=pk, company=company)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != application.status:
            application.status = new_status
            application.save()
            messages.success(request, f"Status updated to: {application.get_status_display()}")
            return redirect('portal:portal_app_detail', pk=pk)
            
    thread_messages = application.messages.all().order_by('created_at')

    # Check if an evaluation already exists for this application
    evaluation = getattr(application, 'evaluation', None)
            
    context = {
        'application': application,
        'status_choices': InternshipApplication.STATUS_CHOICES,
        'thread_messages': thread_messages,
        'evaluation': evaluation,
    }
    return render(request, 'companies/portal/app_detail.html', context)

@login_required
@user_passes_test(is_company_partner, login_url='/accounts/login/')
def submit_evaluation(request, pk):
    """Allow a company partner to submit a performance evaluation for a completed internship."""
    company = request.user.companyprofile.company
    application = get_object_or_404(InternshipApplication, pk=pk, company=company)

    # Guard: only completed internships can be evaluated
    if application.status != 'completed':
        messages.error(request, "Evaluations can only be submitted for completed internships.")
        return redirect('portal:portal_app_detail', pk=pk)

    # Guard: prevent duplicate evaluations
    if hasattr(application, 'evaluation'):
        messages.info(request, "An evaluation has already been submitted for this student.")
        return redirect('portal:portal_app_detail', pk=pk)

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.application = application
            evaluation.evaluator = request.user
            evaluation.review_status = 'pending_review'
            evaluation.save()

            # Notify all admin/staff users for review (student notified after approval)
            admin_users = User.objects.filter(is_staff=True)
            for admin_user in admin_users:
                Notification.objects.create(
                    user=admin_user,
                    title=f"New Evaluation: {application.student.username} at {company.name}",
                    message=f"A performance evaluation has been submitted and requires your review.",
                    link=f"/dashboard/admin/evaluations/{evaluation.pk}/"
                )

            messages.success(request, "Evaluation submitted successfully! It will be reviewed by the university before the student can see it.")
            return redirect('portal:portal_app_detail', pk=pk)
    else:
        form = EvaluationForm()

    context = {
        'form': form,
        'application': application,
        'company': company,
    }
    return render(request, 'companies/portal/submit_evaluation.html', context)

