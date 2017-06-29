# -*- coding: utf-8 -*-
from django import forms
from app.models import *
from django.forms import ModelForm
#define your custom forms here


class ContributionForm(ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'role', 'contribution']

    def __init__(self, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UploadFileForm(forms.Form):
    file = forms.FileField(label='')



