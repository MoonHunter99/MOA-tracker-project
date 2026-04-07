from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentRegistrationForm

# Create your views here.

def register(request):
    # Check if the user is already logged in; if so, send them to the dashboard
    if request.user.is_authenticated:
        return redirect('companies:dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after they register
            login(request, user)
            return redirect('companies:dashboard')
    else:
        form = StudentRegistrationForm()
        
    return render(request, 'registration/register.html', {'form': form})