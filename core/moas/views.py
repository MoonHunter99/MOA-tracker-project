from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MOARequestForm

# Create your views here.

@login_required
def request_moa(request):
    if request.method == 'POST':
        form = MOARequestForm(request.POST)
        if form.is_valid():
            moa_request = form.save(commit=False)
            moa_request.student = request.user
            moa_request.status = 'pending'
            moa_request.save()
            # Redirect back to the dashboard after successfully submitting
            return redirect('companies:dashboard') 
    else:
        form = MOARequestForm()

    context = {
        'form': form,
    }
    return render(request, 'moas/request_moa.html', context)