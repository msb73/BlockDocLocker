from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Post
from django.views.generic.edit import FormView
from .form import FileFieldForm, AddUsersForm
from django.contrib import messages
import json
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_tables2 import SingleTableView
# from .tables import SimpleTable
from django_tables2 import SingleTableView, Table
from django.utils.html import format_html
from .tables import ViewTable  
from .models import DummyModel
import magic
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





def about(request):
    # return HttpResponseRedirect("https://www.google.com")
    # print(request.POST)
    return render(request,'doc/about.html')


def checkRequests(request):
    pass

class AddUser(FormView):
    form_class = AddUsersForm
    template_name = "doc/upload.html"
    success_url = ""
    
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
           return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

class uploadDocuments(FormView):
    form_class = FileFieldForm
    template_name = "doc/upload.html"  # Replace with your template.
    success_url = ""  # Replace with your URL or reverse().
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
           return self.form_valid(form, request) 
        else:
            return self.form_invalid(form) 

    def form_valid(self,form, request): 
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(request.POST) 
        context = {"redirect" : "/documents/", "web3method" : "uploadDocument", "content" : []}
        files = form.cleaned_data["file_field"]
        print(files)
        documentName = request.POST.getlist("documentName")
        caseNo = request.POST.getlist("caseNo")
        documentId = request.POST.getlist("documentId")
        for index, file in enumerate(files): 
            try:
                doctype= file.content_type
                cid = upload(file, "None")
                context["content"].append([
                    documentName[index], caseNo[index], documentId[index], cid, 0, "Document Hash", 1, "0x0000000000000000000000000000000000000000"
                ])
            except Exception as e:
                return HttpResponse(f"Error {e}")
        print(f'{context["content"]=}')
        print(f"executed")
        # context["content"] = []
        # context["content"] = [['JS',2021,232,"Dafsadfasdfcafs",999999,"Sdafdsacsfgs",1,"0x9b7A93538D87fBBBA91b90aA46D2E28D5E5A772b"]]
            
        return render(request, "doc/first.html", context = context) 
    


class ViewDocuments(SingleTableView):
    table_class = ViewTable
    data = []
    model = DummyModel
    template_name = 'doc/viewDocuments.html'
    def get_table_data(self):
        return (ViewDocuments.data)

    def post(self,  request, *args, **kwargs):
        # Access the form data using request.POST
        for i in json.loads(request.POST.get("data")):
            ViewDocuments.data.append({
                'name' : i[0],
                'caseNo' : int(i[1]),
                'documentId' : int(i[2]),
			    'cid' : format_html("<a href = '{}' target='_blank'> Click </a>","https://ipfs.io/ipfs/"+ i[3]),
			    'timeStamp' : i[4],
			    'documentHash' : i[5],
			    'documentType' : i[6], 
            })
        # Process the form data as needed
        # print(self.data)
        # Call the get method to update the table data
        return self.get(request, *args, **kwargs)
    

# class CheckRequests(SingleTableView):
#     table_class = ViewTable
#     data = []

#     model = DummyModel
#     template_name = 'doc/my_list.html'
#     def get_table_data(self):
#         return (CheckRequests.data)

#     def post(self,  request, *args, **kwargs):
#         # Access the form data using request.POST
#         for i in json.loads(request.POST.get("data")):
#             CheckRequests.data.append({
#                 'name' : i[0],
#                 'caseNo' : int(i[1]),
#                 'documentId' : int(i[2]),
# 			    'cid' : i[3],
# 			    'timeStamp' : i[4],
# 			    'documentHash' : format_html("<a href = '{}' target='_blank'> Click </a>","https://ipfs.io/ipfs/"+ i[5]),
# 			    'documentType' : i[6], 
#             })
#         # Process the form data as needed
#         # print(self.dataa)
#         # Call the get method to update the table data
#         return self.get(request, *args, **kwargs)