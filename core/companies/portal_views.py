from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from companies.models import Company
from applications.models import InternshipApplication, ApplicationMessage

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
            
    context = {
        'application': application,
        'status_choices': InternshipApplication.STATUS_CHOICES,
        'thread_messages': thread_messages
    }
    return render(request, 'companies/portal/app_detail.html', context)
