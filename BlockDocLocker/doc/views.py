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

def home(request):
     
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

            uploaded_document = request.FILES['file']
            temp_file = tempfile.NamedTemporaryFile(delete=False)

            for chunk in uploaded_document:
                temp_file.write(chunk)
                
            uuid=ipfs_file.upload((f"{temp_file.name}").replace("\\","/")) 

        if "caseNo" in request.POST:
            form = self.get_form(self.form_class)
            if form.is_valid():
               return self.form_valid(form, request) 
            else:
                return self.form_invalid(form) 

    def form_valid(self,form, request):
        try:
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
            
        form = self.get_form(self.get_form_class()) 
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

def about(request):
    return render(request,'doc/about.html')

def document_retrive(request):
    response=ipfs_file.retrive()
    file_data=response.content
    content_type = response.headers.get('content-type', 'application/octet-stream')
    response = FileResponse(io.BytesIO(file_data), content_type=content_type)
    return response
