from django import forms
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
        print("dasfsd")
        print(data)
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileFieldForm(forms.Form):
    documentName = forms.CharField(widget= forms.TextInput)
    caseNo = forms.CharField(widget= forms.NumberInput)
    file_field = MultipleFileField()
    description = forms.CharField(widget=forms.Textarea({"height" : "30px"}))  
    
    
class AddUsersForm(forms.Form): 
    userId = forms.CharField(widget= forms.TextInput, max_length=42, min_length=42)
    username = forms.CharField(widget=forms.TextInput, max_length=12, min_length=5)
    deptNumber = forms.CharField(widget= forms.NumberInput)
    userType = forms.ChoiceField(choices= ((1, "name" ), (2, "USER" ), ) )

 
class AddCasesForm(forms.Form): 
    def __init__(self, case_data = [], *args, **kwargs):
        super(AddCasesForm, self).__init__(*args, **kwargs)
        self.fields["caseName"] = forms.CharField(widget=forms.TextInput)
        self.fields["caseNo"] = forms.CharField(widget=forms.NumberInput)
        CHOICES = [i for i in case_data]
        self.fields["incharge"] = forms.ChoiceField( widget = fms.Select2Widget(attrs={'style': 'width: 100%;'}, choices = CHOICES))   

class DocumentSelectionForm(forms.Form):
    def __init__(self, case_data, *args, **kwargs):
        super(DocumentSelectionForm, self).__init__(*args, **kwargs)
        # Iterate through case data to dynamically create form fields
        for case_id, documents in case_data.items():
            
            case_field_name = f'case_{case_id}'   
            self.fields[case_field_name] = forms.MultipleChoiceField(
                choices=[(doc[formCheckRequests[0]],
                    format_html("{}  {} {}".format(doc[formCheckRequests[0]], doc[formCheckRequests[1]], f'<div id = "{doc[formCheckRequests[0]]}"> </div>'))) 
                        for doc in documents],
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'document-checkbox', "name" : "ids"}) 
            )
        #             calender = 
        # 
