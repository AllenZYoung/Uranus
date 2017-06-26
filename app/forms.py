# -*- coding: utf-8 -*-
from django import forms


# define your custom forms here

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'placeholder': '请输入用户名', }))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'placeholder': '请输入密码', }))
