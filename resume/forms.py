from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name',
            'experiences',
            'projects',
            'education',
            'skills',
            'contact_website',
            'contact_linkedin',
            'contact_email',  # Only include if your model defines it
            'contact_phone',  # Only include if your model defines it
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'experiences': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_website': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_linkedin': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
