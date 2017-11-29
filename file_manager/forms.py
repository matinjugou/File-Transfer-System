from django import forms

__author__ = "Bifei Yang"


class FileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 1Mb'
    )
    fileType = forms.CharField(
        label='please type in file type'
    )
    validTime = forms.IntegerField(
        label='please type in valid time'
    )
