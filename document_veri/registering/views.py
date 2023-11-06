from django.shortcuts import render, redirect
from django.contrib import messages
from .form import UserRegisterationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method=="POST":
        form = UserRegisterationForm(request.POST,request.Image)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'User created for {username}')
            return redirect('doc-home')

    else:
        form = UserRegisterationForm()
    return render(request, "registering/register.html",{'form':form})

@login_required
def profile(request):
    return render(request, 'registering/profile.html')