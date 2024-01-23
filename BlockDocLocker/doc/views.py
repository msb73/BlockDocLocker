from django.shortcuts import render
from django.views.generic.edit import FormView
from .form import FileFieldForm, AddUsersForm,  SendRequestForm, AddCasesForm, RemoveUsersForm, ChangeInchargeForm
import json
from django.http import HttpResponse
from django_tables2 import SingleTableView
from .tables import ViewTable  , CheckRequestsTable, CheckApprovalsTable
from .models import DummyModel
from .names import *
from .extra import Mapping, UPMapping
from datetime import datetime,  timedelta 

def home(request):
    obj1 = Mapping()
    transact ={
        "function" : "viewDocuments",
        'data' : None
    }
    return render(request, 'doc/home.html', context= {'transact' : json.dumps(transact) })
class AddCases(FormView):
    template_name = "doc/upload.html"
    form_class = AddCasesForm
    success_url = '' 
    def get(self, request, *args, **kwargs):
        if not request.GET:  # if its empty
            context = Mapping.get_context(meth= "allUsers", redirect = "addCases")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data" in request.POST:
            form = self.form_class(case_data = Mapping.down_all_users(data = request.POST.get("data")))
            form.is_bound = False
            return render(request, self.template_name, {'form': form}) 
        
        form = self.get_form(self.form_class)
        if "incharge" in request.POST:
            context = UPMapping.get_context("addCases", func = UPMapping.up_add_cases, data = request.POST)
            return render(request, "doc/first.html", context = context)

class RemoveUsers(FormView): 
    template_name = "doc/upload.html"
    form_class = RemoveUsersForm
    success_url = ''
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:  # if its empty 
            context = Mapping.get_context(meth= "allUsers", redirect = "removeUsers")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data" in request.POST:
            form = self.form_class(case_data = Mapping.down_all_users(data = request.POST.get("data")))
            form.is_bound = False
            return render(request, self.template_name, {'form': form})
        if "users" in request.POST:
            context = UPMapping.get_context("removeUsers", func = UPMapping.up_remove_users, data = request.POST)
            return render(request, "doc/first.html", context = context)
    
class ChangeIncharge(FormView): 
    template_name = "doc/upload.html"
    form_class = ChangeInchargeForm
    success_url = ''
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:  # if its empty 
            context = Mapping.get_context(meth= "allCases", redirect = "changeIncharge")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data" in request.POST:
            form = self.form_class(case_data = Mapping.down_change_incharge(data = request.POST.get("data")))
            form.is_bound = False
            return render(request, self.template_name, {'form': form})
        if "users" in request.POST:
            context = UPMapping.get_context("changeInCharge", func = UPMapping.up_change_incharge, data = request.POST)
            print(context)
            return render(request, "doc/first.html", context = context)

class uploadDocuments(FormView):
    form_class = FileFieldForm
    template_name = "doc/upload.html"  
    success_url = ""
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:  # if its empty 
            context = Mapping.get_context(meth= "userCases", redirect = "uploadDocuments")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data"  in request.POST:
            request.session["case_data"] = Mapping.down_user_cases(request.POST.get("data"))
            form = self.form_class(case_data = request.session["case_data"])
            form.is_bound = False
            return render(request, self.template_name, {"form" : form})
        if "caseNo" in request.POST:
            form = self.get_form(form_class=FileFieldForm)
            print(f'{request.session["case_data"]=}') 
            setattr(form.fields["caseNo"], "choices", request.session["case_data"]) 
            # form.is_bound = False
            if form.is_valid():
                print("valid")
                return self.form_valid(form, request) 
            else:
                print(form.non_field_errors)
                return self.form_invalid(form) 

    def form_valid(self,form, request):
        try: 
            print("ERROR")
            context = UPMapping.get_context("uploadDocument", func = UPMapping.up_upload_documents, data = request.POST, form = form)
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
        context = UPMapping.get_context("addUsers", func = UPMapping.up_add_users, data = request.POST)
        return render(request, "doc/first.html", context = context) 
     
class ViewDocuments(SingleTableView):
    
    table_class, table_data, template_name = ViewTable, [], 'doc/viewDocuments.html'
    model = DummyModel
    
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:  # if its empty 
            context = Mapping.get_context(meth= "viewDocuments", redirect = "viewDocuments")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs) 
    
    def post(self,  request, *args, **kwargs):
        if "data" in request.POST:
            ViewDocuments.table_data =  Mapping.down_view_documents(data = request.POST.get("data"))
        return self.get(request, *args, **kwargs)

class SendRequestView(FormView):
    template_name = 'doc/requests.html'
    form_class = SendRequestForm
    success_url = ''  

    def get(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:  # if its empty 
            context = Mapping.get_context(meth= "allDocuments", redirect = "sendRequests")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "data" in request.POST:
            kwargs = Mapping.down_all_documents(data = request.POST.get("data"))
            form = self.form_class(case_data = Mapping.down_all_documents(data = request.POST.get("data")))
            form.is_bound = False
            date = str((datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
            return render(request, self.template_name, {'form': form, "date" : date })  
            
        form = self.get_form(form_class=SendRequestForm) 
        if "dates" in request.POST: 
            if form.is_valid():
                return self.form_valid(request) 
            else:
                return self.form_invalid(form)
        return HttpResponse("Date not Selected")
    def form_valid(self, request):
        context = UPMapping.get_context("sendRequests", func = UPMapping.up_send_requests, data = request.POST)
        print(context["content"]) 
        return render(request, "doc/first.html", context = context)

class ApproveRequests(SingleTableView): 
    table_data = []
    table_class = CheckApprovalsTable
    model = DummyModel
    template_name = 'doc/viewDocuments.html'
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:  # if its empty 
            context = Mapping.get_context(meth= "checkApprovals", redirect = "checkApprovals")
            return render(request, "doc/first.html", context = context)
        return super().get(self, request, *args, **kwargs)
    
    def post(self,  request, *args, **kwargs):
        if "data" in request.POST:
            ApproveRequests.table_data = Mapping.down_check_approvals(data = request.POST.get("data"))
        if "selected_options" in request.POST:
            context = UPMapping.get_context("approveRequests", func = UPMapping.up_approve_requests, data = request.POST.getlist("selected_options"))
            return render(request, "doc/first.html", context = context)
        return self.get(request, *args, **kwargs)
    
