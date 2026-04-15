from django import forms
from .models import CompanyReview, contains_blocked_content


TAILWIND_INPUT = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm'
TAILWIND_TEXTAREA = TAILWIND_INPUT + ' resize-none'


class CompanyReviewForm(forms.ModelForm):
    """
    Form for submitting a structured internship review.
    Auto-screens text fields against the keyword blocklist during clean().
    """

    class Meta:
        model = CompanyReview
        fields = [
            'overall_rating', 'mentorship_rating', 'work_culture_rating', 'learning_rating',
            'pros', 'cons', 'advice', 'is_anonymous',
        ]
        widgets = {
            'overall_rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'mentorship_rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'work_culture_rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'learning_rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'pros': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3, 'placeholder': 'What did you enjoy most about the internship?'}),
            'cons': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3, 'placeholder': 'What areas could the company improve?'}),
            'advice': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 2, 'placeholder': 'Any tips for future interns? (optional)'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-red-600 shadow-sm focus:ring-red-500'}),
        }

    def clean(self):
        """Auto-moderate: if any text field is flagged, set status to pending_review."""
        cleaned_data = super().clean()
        # Check all text fields against the blocklist
        text_to_check = ' '.join([
            cleaned_data.get('pros', ''),
            cleaned_data.get('cons', ''),
            cleaned_data.get('advice', ''),
        ])

        if contains_blocked_content(text_to_check):
            # Store the flag — the view will read this to set the model status
            cleaned_data['_is_flagged'] = True
        else:
            cleaned_data['_is_flagged'] = False

        return cleaned_data
