from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterationForm(UserCreationForm):
    email=forms.EmailField()
    # image=forms.ImageField()
    PROFILE_TYPE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    profile_type = forms.ChoiceField(
        choices=PROFILE_TYPE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model=User
        fields=['first_name','last_name','profile_type','username','email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }