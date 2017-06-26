# -*- coding: utf-8 -*-
#define your utility function here

from . import models
from django.contrib.auth.models import User

def auth_user(form):
    if form.is_valid():
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        # check
        user = models.Student.objects.filter(username=username, password=password)
        if user:
            return True
        else:
            return False
    else:
        return False