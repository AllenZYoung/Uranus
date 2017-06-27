# -*- coding: utf-8 -*-
from django import forms


# define your custom forms here

class UploadFileForm(forms.Form):
    file = forms.FileField()
