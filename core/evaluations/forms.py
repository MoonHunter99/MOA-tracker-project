from django import forms
from .models import InternshipEvaluation


SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]


class EvaluationForm(forms.ModelForm):
    """
    Form for company partners to submit structured internship evaluations.
    Uses radio-button widgets for each 1-5 rating criterion.
    """

    technical_skills = forms.ChoiceField(
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label="Technical Skills"
    )
    communication = forms.ChoiceField(
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label="Communication"
    )
    professionalism = forms.ChoiceField(
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label="Professionalism"
    )
    teamwork = forms.ChoiceField(
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label="Teamwork"
    )
    initiative = forms.ChoiceField(
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label="Initiative"
    )

    class Meta:
        model = InternshipEvaluation
        fields = [
            'technical_skills', 'communication', 'professionalism',
            'teamwork', 'initiative', 'overall_comments', 'recommendation'
        ]
        widgets = {
            'overall_comments': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Provide overall feedback on the student\'s performance during their internship...',
                'class': 'mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md focus:ring-red-500 focus:border-red-500'
            }),
            'recommendation': forms.Select(attrs={
                'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm rounded-md'
            }),
        }

    def clean(self):
        """Convert ChoiceField string values back to integers for the model."""
        cleaned_data = super().clean()
        for field in ['technical_skills', 'communication', 'professionalism', 'teamwork', 'initiative']:
            if field in cleaned_data:
                cleaned_data[field] = int(cleaned_data[field])
        return cleaned_data
