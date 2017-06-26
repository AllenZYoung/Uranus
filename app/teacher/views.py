from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from app.models import *


# Create your views here.
@login_required(login_url='app:login')
def index(request):
    user=request.user
    #教师首页默认显示该教师的所有课程
    enrolls=Enroll.objects.filter(user__username=user.username)
    courses=[]
    for enroll in enrolls:
        courses.append(enroll.course)
    teacher=User.objects.filter(username=user.username)
    return render(request, 'teacher/teacher_index.html', {'courses': courses, 'teacher':teacher})


def create_homework(request):
    return HttpResponse('create homework')


def edit_course(request):
    return HttpResponse('edit course')


def edit_homework(request):
    return HttpResponse('edit homework')