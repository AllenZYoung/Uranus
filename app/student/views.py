from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#TODO 学生登录和注销（一般而言，要与教师、教务统一）

# Create your views here.
def index(request):
    return HttpResponse('student page')



@login_required(login_url='app:login')
def member_evaluation(request): # （团队负责人）学生的成员评价页面
    return HttpResponse('Member Evaluation here.')

@login_required(login_url='app:login')
def work_submit(request): # （团队负责人）学生的作业提交页面
    return HttpResponse('Submit your group\'s homework here.')
