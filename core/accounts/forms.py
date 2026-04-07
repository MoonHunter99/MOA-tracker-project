from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm'}))
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm'}))
    
    student_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm', 'placeholder': 'e.g. 2022-00001-MN-0'}))
    course = forms.ChoiceField(choices=StudentProfile.COURSE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm'}))
    year_level = forms.ChoiceField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year'), (5, '5th Year')], required=True, widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # The signal will create the StudentProfile, now we update it
            user.profile.student_number = self.cleaned_data['student_number']
            user.profile.course = self.cleaned_data['course']
            user.profile.year_level = self.cleaned_data['year_level']
            user.profile.save()
        return user
