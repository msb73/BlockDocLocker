from typing import Any
from django.shortcuts import render
from .models import Post
from django.views.generic.edit import FormView
from .form import FileFieldForm, AddUsersForm,  DocumentSelectionForm, AddCasesForm
import json
from django.urls import reverse
from django.http import HttpResponse
from django_tables2 import SingleTableView
from django.utils.html import format_html
from .tables import ViewTable  , CheckRequestsTable, CheckApprovalsTable
from .models import DummyModel
from .ipfs import upload
from .extra import Mapping, UPMapping
from datetime import datetime,  timedelta 

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
                        # cid = upload(file, "None")
                        cid = "true"
                        if cid: break
                    else:   raise ValueError(f"CID cannot be created please try later  {file.name}")
                    context["content"].append([
                        documentName[index], caseNo[index], 0000000, cid, 0000000, doctype , "0x0000000000000000000000000000000000000000"
                    ])
        except Exception as e:
            return HttpResponse(f"Error {e}")
        return render(request, "doc/first.html", context = context) 
    
class AddUser(FormView):
    template_name = "doc/upload.html"
    form_class = AddUsersForm
    success_url = ""
    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
           return self.form_valid(request) 
        else:
            return self.form_invalid(form) 
        
    def form_valid(self, request):
        
        userId = request.POST.getlist("userId")
        username = request.POST.getlist("username")
        deptNumber = request.POST.getlist("deptNumber")
        userType = request.POST.getlist("userType")
        context = {"web3method" : "addUsers", "content" : []}
        for i in range(len(username)):
            context["content"].append([
                userId[i], userType[i], username[i], deptNumber[i]
            ])
        return render(request, "doc/first.html", context = context) 
    
    
class ViewDocuments(SingleTableView):
    table_class, table_data, template_name = ViewTable, [], 'doc/viewDocuments.html'
    model = DummyModel
    def get(self, request, *args, **kwargs):
        # return super().get(self, request, *args, **kwargs)
        if request.GET.get("meth"):
            return render(request, "doc/first.html", context = Mapping.get_context(context = request.GET.get("meth")))
        return super().get(self, request, *args, **kwargs) 
    
    def post(self,  request, *args, **kwargs):
        if "data" in request.POST:
            ViewDocuments.table_data =  Mapping.down_view_documents(data = request.POST.get("data"))
        return self.get(request, *args, **kwargs) 


# approveRequests 
class SendRequestView(FormView):
    template_name = 'doc/requests.html'
    form_class = DocumentSelectionForm
    success_url = ''  
    def get_form_kwargs(self, case_data = {}):
        kwargs = super().get_form_kwargs()
        kwargs['case_data'] = case_data
        return kwargs
    
    def get(self, request, *args, **kwargs):
        if "meth" in request.GET:
            context = Mapping.get_context(context= request.GET.get("meth"))
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data" in request.POST:
            kwargs = self.get_form_kwargs(case_data=Mapping.down_all_documents(data = request.POST.get("data")))
            form = self.form_class(**kwargs)
            date = str((datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
            return render(request, self.template_name, {'form': form, "date" : date })
        if request.POST:    
            form = self.get_form(self.get_form_class()) 
            
            
            # print(list(request.POST.items()))
            # for i, j in  request.POST.items():
                
            #     print(request.POST.getlist(i))
            if form.is_valid():
                return self.form_valid(request) 
            else:
                return self.form_invalid(form) 
                
    def form_valid(self, request):
        context = UPMapping.get_context("sendRequests", func = UPMapping.up_send_requests, data = request.POST)
        print(context["content"]) 
        return render(request, "doc/first.html", context = context)



def removeUsers(request):
    ...

class ApproveRequests(SingleTableView): 
    table_data = []
    table_class = CheckApprovalsTable
    model = DummyModel
    template_name = 'doc/viewDocuments.html'
    
    def get(self, request, *args, **kwargs):
        if "meth" in request.GET:
            context = Mapping.get_context(context = request.GET.get("meth"))
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self,  request, *args, **kwargs):
        if "data" in request.POST:
            ApproveRequests.table_data = Mapping.down_check_approvals(data = request.POST.get("data"))
        if "selected_options" in request.POST:
            context = {"web3method" : "approveRequests", 
                "content" : UPMapping.up_approve_requests(data = request.POST.getlist("selected_options"))}
            return render(request, "doc/first.html", context = context)
        
        return self.get(request, *args, **kwargs)
    
    
    
class CSRequestView(FormView):
    template_name = "doc/upload.html"
    form_class = AddCasesForm
    success_url = '' 
    def get(self, request, *args, **kwargs):
        if "meth" in request.GET:
            context = Mapping.get_context(context= request.GET.get("meth"))
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data" in request.POST:
            print(json.loads(request.POST.get("data")))
            case_data = []
            for address, name in zip(json.loads(request.POST.get("data"))["0"],json.loads(request.POST.get("data"))["1"]):
                case_data.append((address, name + "    -   " + address))
            kwargs = super().get_form_kwargs()
            kwargs['case_data'] = case_data
            form = AddCasesForm(**kwargs)
            return render(request, self.template_name, {'form': form})
    def form_valid(self, request):
        form = request.POST
        print("form enced")
        # if checkRequest gives approveRequests
        if request.POST.get("method") == "checkRequests":
            context = {"web3method" : "approveRequests", "content" : []}
        else:
            context = {"web3method" : "sendRequests", "content" : []} 
        ls = form.lists()
        next(ls)
        context["content"] = [i for j in ls for i in j]
        return render(request, "doc/first.html", context = context)


