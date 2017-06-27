# -*- coding: utf-8 -*-
from django import forms

#define your custom forms here

class FileForm(forms.Form):
    filefield = forms.FileField(required=True, label='请选择文件')