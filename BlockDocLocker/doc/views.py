from django.shortcuts import render, redirect
from .models import Post
from .form import UploadFileForm
from django.contrib import messages
from django.http import FileResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from ipfs import ipfs_file
import io
import os
import tempfile


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
            temp_file = tempfile.NamedTemporaryFile(delete=False)

            for chunk in uploaded_document:
                temp_file.write(chunk)
                
            uuid=ipfs_file.upload((f"{temp_file.name}").replace("\\","/")) 

            Post(uname=request.user,document=form.cleaned_data['Document_Name'],uid=uuid).save()

            messages.success(request, f'Document Uploaded Successfully')
            return redirect('doc-home')
    else:
        form = UploadFileForm()

    return render(request, 'doc/upload.html', {'form': form})

def about(request):
    return render(request,'doc/about.html')

def document_retrive(request):
    response=ipfs_file.retrive()
    file_data=response.content
    content_type = response.headers.get('content-type', 'application/octet-stream')
    response = FileResponse(io.BytesIO(file_data), content_type=content_type)
    return response