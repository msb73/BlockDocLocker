from django.shortcuts import render, redirect
from .models import Post
from .form import UploadFileForm
from django.contrib import messages


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        name=request.user.username
        context={
            "posts":Post.objects.filter(uname__username=name)
        }
        return render(request, 'doc/home.html', context)
    return render(request, 'doc/home.html')

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            uploaded_document = request.FILES['file']
            
            ##output = your_document_processing_function(uploaded_document)

            uuid='Gig8149'

            Post(uname=request.user,document=form.cleaned_data['Document_Name'],uid=uuid).save()

            messages.success(request, f'Document Uploaded Successfully')
            return redirect('doc-home')
    else:
        form = UploadFileForm()

    return render(request, 'doc/upload.html', {'form': form})

def about(request):
    return render(request,'doc/about.html')