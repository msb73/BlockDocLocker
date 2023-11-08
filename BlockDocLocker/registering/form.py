from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterationForm(UserCreationForm):
    email=forms.EmailField()
    # image=forms.ImageField()
    PROFILE_TYPE_CHOICES = [
        ('User', 'User'),
        ('Agent', 'Agent'),
    ]

    profile_type = forms.ChoiceField(
        choices=PROFILE_TYPE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model=User
        fields=['first_name','last_name','profile_type','username','email', 'password1', 'password2']