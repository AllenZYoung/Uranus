# -*- coding: utf-8 -*-
from django import forms


# define your custom forms here

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'placeholder': '请输入用户名', }))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'placeholder': '请输入密码', }))


class UserChangeForm(forms.Form):
    tel = forms.CharField(max_length=16, required=False, label='电话')
    email = forms.EmailField(required=False, label='邮箱')
    passwd = forms.CharField(max_length=32, required=False, label='密码', widget=forms.PasswordInput(attrs={'placeholder': '不填写则不更改密码', }))
    second_passwd = forms.CharField(max_length=32, required=False, label='再次输入密码',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name is not 'attachment':
                field.widget.attrs['class'] = 'form-control'

