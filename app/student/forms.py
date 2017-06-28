# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.forms import ModelForm
#define your custom forms here


class ContributionForm(ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'role', 'contribution']
