from typing import Any
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Post
from django.views.generic.edit import FormView
from .form import FileFieldForm, AddUsersForm,  DocumentSelectionForm
from django.contrib import messages
import json
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_tables2 import SingleTableView
from django.utils.html import format_html
from .tables import ViewTable  , RequestTable
from .models import DummyModel
import io
import os
import tempfile
from .ipfs import upload, retrive
import datetime as dt

# # Create your views here.
# def first(request):
#     context = {"web3method" : None,
#                    "redirect" : None}
#     if request.method == "GET":
#         if request.GET.get("meth"):
#             print("get called")
#             context = {"web3method" : request.GET.get("meth"),
#                    "redirect" : reverse(request.GET.get("meth"))}
#             print(context["redirect"])
#     return render(request, "doc/first.html", context = context)
def home(request):
     
    transact ={
        "function" : "viewDocuments",
        'data' : None
    }
    return render(request, 'doc/home.html', context= {'transact' : json.dumps(transact) })




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
        context = {"web3method" : "uploadDocument", "content" : []}
        files = form.cleaned_data["file_field"]
        print(files)
        documentName = request.POST.getlist("documentName")
        caseNo = request.POST.getlist("caseNo")
        documentId = request.POST.getlist("documentId")
        try:
            for index, file in enumerate(files): 

                    doctype= file.content_type
                    for _ in range(3):
                        cid = upload(file, "None")
                        if cid: break
                    else:   raise ValueError(f"CID cannot be created please try later  {file.name}")
                    context["content"].append([
                        documentName[index], caseNo[index], documentId[index], cid, 0, "Document Hash", 1, "0x0000000000000000000000000000000000000000"
                    ])
        except Exception as e:
            return HttpResponse(f"Error {e}")
        return render(request, "doc/first.html", context = context) 
    
class AddUser(FormView):
    template_name = "doc/upload.html"
    form_class = AddUsersForm
    success_url = ""
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
           return self.form_valid(form, request) 
        else:
            return self.form_invalid(form) 
        
    def form_valid(self, request):
        username = request.POST.getlist("userId")
        userId = request.POST.getlist("username")
        deptNumber = request.POST.getlist("deptNumber")
        userType = request.POST.getlist("userType")
        context = {"web3method" : "addUsers", "content" : []}
        for i in range(len(username)):
            context["content"].append([
                userId[i], userType[i], username[i], deptNumber, True
            ])
        return render(request, "doc/first.html", context = context) 
    
    
class ViewDocuments(SingleTableView):
    table_class = ViewTable
    table_data = []
    model = DummyModel
    template_name = 'doc/viewDocuments.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get("meth"):
            context = {"web3method" : request.GET.get("meth"),
                   "redirect" : reverse(request.GET.get("meth"))}
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self,  request, *args, **kwargs):
        if not self.table_data:
            for i in json.loads(request.POST.get("data")):
                self.table_data.append({
                    'name' : i[0],
                    'caseNo' : int(i[1]),
                    'documentId' : int(i[2]),
		    	    'cid' : format_html("<a href = '{}' target='_blank'> Click </a>","https://ipfs.io/ipfs/"+ i[3]),
		    	    'timeStamp' : dt.datetime.fromtimestamp((int)(i[4])),
		    	    'documentHash' : i[5],
		    	    'documentType' : i[6], 
                })
        return self.get(request, *args, **kwargs)


# approveRequests 
class CSARequestView(FormView):
    template_name = 'doc/requests.html'
    form_class = DocumentSelectionForm
    success_url = ''  
    def get_form_kwargs(self, case_data = {}):
        kwargs = super().get_form_kwargs()
        kwargs['case_data'] = case_data
        return kwargs
    
    def get(self, request, *args, **kwargs):
        if request.GET.get("meth"):
            context = {"web3method" : request.GET.get("meth"),
                   "redirect" : reverse(request.GET.get("meth"))}
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)   
    
    def post(self, request, *args, **kwargs):
        if request.POST.get("data"):
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(request.POST.get("data"))
            print(json.loads(request.POST.get("data")))
            data = {}
            for i in json.loads(request.POST.get("data")):
                caseId = i[3][4:]
                if data[caseId]:
                    data[i["Caseid"]].append({ "documentId" : i["documentId"] , "issuer" : i["issuer"] })
                else:
                    data[caseId] = [{
                        "index" : i[0], 
                        "address" : i[1],
                        "issuerName" : i[2], 
                        "documentId" : i[3], 
                        "documentName" :i[4], 
                        "timestamp" :dt.datetime.fromtimestamp((int)(i[5])) , 
                        "AskedTime" : dt.datetime.fromtimestamp((int)(i[6])),
                        }]
               
            case_data = {
                'case1': [{'documentId': 'doc1', 'issuer': 'Issuer1'}, {'documentId': 'doc2', 'issuer': 'Issuer2'}],
                'case2': [{'documentId': 'doc3', 'issuer': 'Issuer3'}, {'documentId': 'doc4', 'issuer': 'Issuer4'}],
            }
            kwargs = self.get_form_kwargs(case_data=case_data)
            form = DocumentSelectionForm(**kwargs)
            return render(request, self.template_name, {'form': form})
            
        form = self.get_form(self.get_form_class())
        if form.is_valid():
           return self.form_valid(request) 
        else:
            return self.form_invalid(form) 
        
    def form_valid(self, request):
        form = request.POST
        # if checkRequest gives approveRequests
        if request.POST.get("method") == "checkRequests":
            context = {"web3method" : "approveRequests", "content" : []}
        else:
            context = {"web3method" : "sendRequests", "content" : []} 
        ls = form.lists()
        next(ls)
        context["content"] = [i for j in ls for i in j]
        return render(request, "doc/first.html", context = context)



def removeUsers(request):
    ...
    
class Requests(SingleTableView):
    table_class = RequestTable
    table_data = []
    model = DummyModel
    template_name = 'doc/viewDocuments.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get("meth"):
            context = {"web3method" : request.GET.get("meth"),
                   "redirect" : reverse(request.GET.get("meth"))}
            return render(request, "doc/first.html", context = context)
        if request.GET.get("selected_options"):
            print(f"$$$$$$$$$$$$$$$$$${request.GET.get('selected_options')}")
        return super().get(self, request, *args, **kwargs)
    
    def post(self,  request, *args, **kwargs):
        try:
            if not self.table_data:
                for i in json.loads(request.POST.get("data")):
                    self.table_data.append({
                            "documentId" : i[3], 
                            "documentName" :i[4], 
                            "issuerName" : i[2],
                            "timestamp" :dt.datetime.fromtimestamp((int)(i[5])) , 
                            "AskedTime" : dt.datetime.fromtimestamp((int)(i[6])),
		        	        "CheckBox" : format_html(f"<input type='checkbox' id='option{i[0]}' name='selected_options' value='{i[0]}' onclick='updateSessionStorage(this)'> "), 
                    })
            if request.POST.get("selected_options"):
                print(request.POST.getlist("selected_options"))
                context = {"web3method" : "approveRequests", "content" : [int(i) for i in request.POST.getlist("selected_options")]}
                # 
                return render(request, "doc/first.html", context = context)
        except Exception as e: 
            return HttpResponse(f"Error Occured {e}")
        return self.get(request, *args, **kwargs)