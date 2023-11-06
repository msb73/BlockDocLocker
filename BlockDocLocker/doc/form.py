from django import forms


class UploadFileForm(forms.Form):
    Document_Name = forms.CharField(max_length=50)
    file = forms.FileField()