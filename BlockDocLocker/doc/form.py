from django import forms


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

			# string documentName;
			# uint256 caseNo;  // deptNumber + CaseNo
			# uint256 documentId; // caseNo + Increment
			# string _cid;
			# uint256 _timeStamp;
			# string _documentHash;
			# DocType _documentType;
			# address _issuer;

class FileFieldForm(forms.Form):
    documentName = forms.CharField(widget= forms.TextInput)
    caseNo = forms.CharField(widget= forms.NumberInput)
    documentId = forms.CharField(widget= forms.NumberInput)
    # timeStamp = forms.CharField(widget= forms.NumberInput({"value" : 0, "hidden" : "on"})) 
    # documentType = forms.ChoiceField(choices=  (
    #     ("Audio", "Audio" ),
    #     ("Video", "Video" ),
    #     ("Document", "Document")
    # )  ) 
    file_field = MultipleFileField()
    description = forms.CharField(widget=forms.Textarea)
    
    
class AddUsersForm(forms.Form):
    userId = forms.CharField(widget= forms.TextInput, max_length=42, min_length=42)
    userType = forms.ChoiceField(choices=  (
        (1, "ISSUER" ),
        (2, "USER" )
    )  ) 
    username = forms.CharField(widget=forms.TextInput, max_length=12, min_length=5)
    deptNumber = forms.CharField(widget= forms.NumberInput)
    