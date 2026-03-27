from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InternshipApplication
from .forms import ApplicationForm
from companies.models import Company

# Create your views here.

@login_required 
def apply_to_company(request, company_id):
    company = get_object_or_404(Company, id=company_id, is_active=True)
    
    # Optional: Prevent the student from applying twice
    if InternshipApplication.objects.filter(student=request.user, company=company).exists():
        # If they already applied, just redirect them back to the detail page
        return redirect('companies:company_detail', pk=company.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the application object but don't save to the database just yet
            application = form.save(commit=False)
            # Attach the current user and the company to the application
            application.student = request.user
            application.company = company
            application.status = 'submitted'
            # Now save it!
            application.save()
            return redirect('companies:company_detail', pk=company.id)
    else:
        form = ApplicationForm()

    context = {
        'form': form,
        'company': company,
    }
    return render(request, 'applications/apply.html', context)