# accounts/forms.py
from django import forms
from backend_crud.models import Skill, UserSkill
from django.contrib.auth import get_user_model
User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'dob', 'gender', 'education', 'experience']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['skills'].initial = user.user_skill.values_list('skill_id', flat=True)
