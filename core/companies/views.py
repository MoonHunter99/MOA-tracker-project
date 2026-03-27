from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Company
from applications.models import StudentProfile

# Create your views here.
@login_required
def company_list(request):
    # 1. Get the current user's profile
    # we use try/except in case a superuser doesn't have a profile yet
    try:
        user_profile = StudentProfile.objects.get(user=request.user)
        user_course = user_profile.course
        # 2. Filter companies by that course
        companies = Company.objects.filter(course_tag=user_course, status='ACTIVE')
    except StudentProfile.DoesNotExist:
        # If no profile (like for Admin), show all active ones
        companies = Company.objects.filter(status='ACTIVE')
        user_course = "All"

    return render(request, 'companies/company_list.html', {
        'companies': companies,
        'user_course': user_course
    })