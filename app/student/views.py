from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

#TODO 学生登录和注销（一般而言，要与教师、教务统一）

# Create your views here.
def index(request):
    return HttpResponse('student page')

def login(request):
    if request.method == 'POST':
        pass
    return
