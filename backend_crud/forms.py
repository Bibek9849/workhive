from django import forms
from .models import User, Skill

class ProfileUpdateForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'dob', 'phone_no', 'gender',
            'experience', 'education', 'image', 'skills'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
