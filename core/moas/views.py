from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MOARequestForm
from .models import MOARequest
from django.contrib.auth.models import User
from notifications.models import Notification

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

            # Notify all admin/staff users about the new MOA request
            admin_users = User.objects.filter(is_staff=True)
            for admin_user in admin_users:
                Notification.objects.create(
                    user=admin_user,
                    title=f"New MOA Request: {moa_request.target_company_name}",
                    message=f"{request.user.username} requested a new MOA with {moa_request.target_company_name}.",
                    link=f"/dashboard/admin/moas/{moa_request.pk}/"
                )
            # Redirect to the new tracker page after successfully submitting
            return redirect('moas:my_moa_requests') 
    else:
        form = MOARequestForm()

    context = {
        'form': form,
    }
    return render(request, 'moas/request_moa.html', context)

@login_required
def my_moa_requests(request):
    # Fetch all MOA requests for the logged-in user, ordered by newest first
    requests = MOARequest.objects.filter(student=request.user).order_by('-date_requested')
    
    context = {
        'requests': requests,
    }
    return render(request, 'moas/my_moa_requests.html', context)