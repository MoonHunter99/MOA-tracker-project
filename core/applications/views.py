from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from .models import StudentProfile 




# Create your views here.

# 2. Now define the Form that uses that model
class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=16, 
        label="Username / Student Number",
        help_text="Required. 16 characters or fewer."
    )
    
    # This works now because StudentProfile was imported above
    course = forms.ChoiceField(choices=StudentProfile.COURSE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "course")

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Save the User
            user = form.save()
            
            # Create the associated StudentProfile
            course_selected = form.cleaned_data.get('course')
            StudentProfile.objects.create(user=user, course=course_selected)
            
            messages.success(request, f'Account created! You can now login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})