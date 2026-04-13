from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InternshipApplication, ApplicationMessage
from .forms import ApplicationForm
from companies.models import Company
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
            return redirect('applications:application_detail', pk=pk)
            
    thread_messages = application.messages.all().order_by('created_at')
    
    context = {
        'application': application,
        'thread_messages': thread_messages
    }
    return render(request, 'applications/application_detail.html', context)