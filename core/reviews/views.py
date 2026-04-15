from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.models import User
from applications.models import InternshipApplication
from companies.models import Company
from notifications.models import Notification
from .models import CompanyReview
from .forms import CompanyReviewForm


@login_required
def submit_review(request, application_id):
    """Submit a review for a completed internship."""
    application = get_object_or_404(
        InternshipApplication, pk=application_id, student=request.user
    )

    # Only allow reviews for completed internships
    if application.status != 'completed':
        messages.error(request, 'You can only review internships that have been completed.')
        return redirect('applications:application_detail', pk=application.pk)

    # Prevent duplicate reviews
    if hasattr(application, 'review'):
        messages.info(request, 'You have already submitted a review for this internship.')
        return redirect('applications:application_detail', pk=application.pk)

    if request.method == 'POST':
        form = CompanyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.company = application.company
            review.application = application

            # Set status based on auto-moderation result
            if form.cleaned_data.get('_is_flagged', False):
                review.status = 'pending_review'
                messages.info(
                    request,
                    'Thank you! Your review has been submitted and is pending a brief admin review before it goes live.'
                )
                # Notify admins about the flagged review
                admin_users = User.objects.filter(is_staff=True)
                for admin_user in admin_users:
                    Notification.objects.create(
                        user=admin_user,
                        title=f"Flagged Review: {application.company.name}",
                        message=f"A review by {request.user.username} was auto-flagged and needs manual review.",
                        link=f"/dashboard/admin/reviews/{review.pk}/"  # will be wired in admin
                    )
            else:
                review.status = 'approved'
                messages.success(request, 'Your review has been published! Thank you for sharing your experience.')

            review.save()
            return redirect('applications:application_detail', pk=application.pk)
    else:
        form = CompanyReviewForm()

    context = {
        'form': form,
        'application': application,
    }
    return render(request, 'reviews/submit_review.html', context)


def company_reviews(request, company_id):
    """Public listing of all approved reviews for a company."""
    company = get_object_or_404(Company, pk=company_id, is_active=True)

    reviews = CompanyReview.objects.filter(
        company=company, status='approved'
    ).select_related('student', 'application')

    # Calculate aggregate ratings
    avg_ratings = reviews.aggregate(
        avg_overall=Avg('overall_rating'),
        avg_mentorship=Avg('mentorship_rating'),
        avg_culture=Avg('work_culture_rating'),
        avg_learning=Avg('learning_rating'),
    )

    # Round the averages for display
    for key in avg_ratings:
        if avg_ratings[key] is not None:
            avg_ratings[key] = round(avg_ratings[key], 1)

    context = {
        'company': company,
        'reviews': reviews,
        'review_count': reviews.count(),
        'avg_ratings': avg_ratings,
    }
    return render(request, 'reviews/company_reviews.html', context)
