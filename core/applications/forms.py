from django import forms
from .models import InternshipApplication

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ['student_resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm', 
                'rows': 5,
                'placeholder': 'Explain why you are a good fit for this company...'
            }),
            'student_resume': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
            })
        }