from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterationForm(UserCreationForm):
    email=forms.EmailField()
    image=forms.ImageField()

    class Meta:
        model=User
        fields=['first_name','last_name', 'image','username','email', 'password1', 'password2']