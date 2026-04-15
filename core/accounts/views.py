from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentProfileForm, ResumeUploadForm

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


@login_required
def profile_view(request):
    """Display the student's full profile with skills, links, and resume history."""
    profile = request.user.profile
    resumes = profile.resumes.all()  # ordered by -uploaded_at via model Meta

    context = {
        'profile': profile,
        'resumes': resumes,
        'skills_list': profile.get_skills_list(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """Edit profile fields and optionally upload a new resume version."""
    profile = request.user.profile

    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, instance=profile)
        resume_form = ResumeUploadForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile_form.save()

            # Only process resume if a file was actually uploaded
            if request.FILES.get('file'):
                if resume_form.is_valid():
                    # Deactivate all previous resumes
                    profile.resumes.update(is_active=False)
                    # Save the new resume linked to this profile
                    new_resume = resume_form.save(commit=False)
                    new_resume.profile = profile
                    new_resume.is_active = True
                    new_resume.save()
                    messages.success(request, 'Profile updated and new resume uploaded!')
                else:
                    messages.warning(request, 'Profile updated but there was an issue with the resume file.')
            else:
                messages.success(request, 'Profile updated successfully!')

            return redirect('accounts:profile')
    else:
        profile_form = StudentProfileForm(instance=profile)
        resume_form = ResumeUploadForm()

    context = {
        'profile_form': profile_form,
        'resume_form': resume_form,
    }
    return render(request, 'accounts/edit_profile.html', context)