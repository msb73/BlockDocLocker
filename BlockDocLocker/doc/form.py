from typing import Any, Mapping
from django import forms
from django.forms.utils import ErrorList
from django.utils.html import format_html
from django_select2 import forms as fms
from .names import *
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField): 
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': False}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileFieldForm(forms.Form):
    def __init__(self, *args,case_data = [], **kwargs):
        self.case_data = case_data
        super(FileFieldForm, self).__init__(*args, **kwargs)
        print(self.case_data)
        self.fields[formUploadDocuments[0]] = forms.CharField(widget= forms.TextInput)
        self.fields[formUploadDocuments[1]] = forms.ChoiceField( widget = fms.Select2Widget(attrs={'style': 'width: 100%;'}), choices = self.case_data)
        self.fields[formUploadDocuments[2]] = MultipleFileField()
        self.fields[formUploadDocuments[3]] = forms.CharField(widget=forms.Textarea({"height" : "30px"}))  
    
     
class AddUsersForm(forms.Form): 
    userId = forms.CharField(widget= forms.TextInput, max_length=42, min_length=42)
    username = forms.CharField(widget=forms.TextInput, max_length=12, min_length=5)
    deptNumber = forms.CharField(widget= forms.NumberInput)
    userType = forms.ChoiceField(choices= ((1, "name" ), (2, "USER" ), ) )


        
 
class AddCasesForm(forms.Form): 
    def __init__(self, case_data = [], *args, **kwargs):
        super(AddCasesForm, self).__init__(*args, **kwargs)
        self.fields[formAddCases[0]] = forms.CharField(widget=forms.TextInput)
        self.fields[formAddCases[1]] = forms.CharField(widget=forms.NumberInput)

        self.fields[formAddCases[2]] = forms.ChoiceField( widget = fms.Select2Widget(attrs={'style': 'width: 100%;'}), choices = case_data)

class SendRequestForm(forms.Form):
    def __init__(self, case_data, *args, **kwargs):
        super(SendRequestForm, self).__init__(*args, **kwargs)
        # Iterate through case data to dynamically create form fields
        for case_id, documents in case_data.items():
            case_field_name = f'case_{case_id}'   
            self.fields[case_field_name] = forms.MultipleChoiceField(
                choices=[(doc[formCheckRequests[0]],
                    format_html("{}  {} {}".format(doc[formCheckRequests[0]], doc[formCheckRequests[1]], f'<div id = "{doc[formCheckRequests[0]]}"> </div>'))) 
                        for doc in documents],
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'document-checkbox', "name" : "ids"}) 
            )

class RemoveUsersForm(forms.Form): 
    def __init__(self, case_data = [], *args, **kwargs):
        super(RemoveUsersForm, self).__init__(*args, **kwargs)
        self.case_data = case_data 
        self.fields["users"] = forms.ChoiceField( widget = fms.Select2MultipleWidget(attrs={'style': 'width: 100%;'}), choices = self.case_data)
        
class ChangeInchargeForm(forms.Form):
    def __init__(self, case_data = [], *args, **kwargs):
        super(ChangeInchargeForm, self).__init__(*args, **kwargs) 
        self.fields[formChangeIncharge[0]] = forms.ChoiceField( widget = fms.Select2Widget(), choices = case_data[0])
        self.fields[formChangeIncharge[1]] = forms.ChoiceField( widget = fms.Select2Widget(), choices = case_data[1]) 
        

# </select>