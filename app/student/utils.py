# -*- coding: utf-8 -*-
#define your utility function here

from . import models
from django.contrib.auth.models import User
from .models import *

def auth_user(form): # 瞎写的东西
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

def submit_homework_file(form):  # 提交某个作业（的文件）
    pass

def set_members_evaluations(form): # 为团队成员设置贡献度（可以理解为权重）
    pass

