from django import forms
from .models import MOARequest

class MOARequestForm(forms.ModelForm):
    class Meta:
        model = MOARequest
        fields = ['target_company_name', 'company_contact_person', 'company_contact_email', 'justification']
        widgets = {
            'target_company_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm',
                'placeholder': 'e.g., Tech Innovations Inc.'
            }),
            'company_contact_person': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm',
                'placeholder': 'e.g., Jane Doe, HR Manager'
            }),
            'company_contact_email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm',
                'placeholder': 'hr@techinnovations.com'
            }),
            'justification': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm',
                'rows': 4,
                'placeholder': 'Why do you want to intern here? How does it align with your degree?'
            }),
        }