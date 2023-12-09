from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Post
from django.views.generic.edit import FormView
from .form import FileFieldForm
from django.contrib import messages
import json
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

import io
import os
import tempfile
from .ipfs import upload, retrive

# Create your views here.
def first(request):
    if request.method == "POST":
        web3method = request.POST.get("web3method")
        context = {"web3method" : request.POST.get("web3method"),
               "redirect" : reverse(web3method)}
    else :
        context = {"web3method" : "viewDocuments",
                   "redirect" : reverse("viewDocuments")}
    return render(request, "doc/first.html", context = context)
 
def home(request):
    
    transact ={
        "function" : "viewDocuments",
        'data' : None
    }
    return render(request, 'doc/home.html', context= {'transact' : json.dumps(transact) })

def viewDocuments(request):
    # data = request.POST.get("data")
    print(request.POST.get("data"))
    data = json.loads(request.POST.get("data"))
    # data = request.POST.get("data")
    print(type(data))
    print(data[0][0])
    print(json)
    return render(request, 'doc/viewDocuments.html', context = {"datas" : data})



def about(request):
    # return HttpResponseRedirect("https://www.google.com")
    # print(request.POST)
    return render(request,'doc/about.html')





class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "doc/upload.html"  # Replace with your template.
    success_url = ""  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        print('@@@@@@@@@@@@@@@##############################@@@@@@@@@@@@@@@@@@@')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
           return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self,request, form):
        files = form.cleaned_data["file_field"]
        context = {}
        context["redirect"] = "/viewDocuments/"
        context["web3method"] = "uploadDocuments"
        context["content"] = []
        for file in files:
            try:
                print(file.name)
                context["content"].append(upload(file))
            except Exception as e:
                return HttpResponse(f"Error {e}")
        print(f"executed")
        
        return render(request, "doc/first.html", context = context)