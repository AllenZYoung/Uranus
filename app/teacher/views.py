from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from app.models import *


# Create your views here.
@login_required(login_url='app:login')
def index(request):
    user = request.user
    # 教师首页默认显示该教师的所有课程
    enrolls = Enroll.objects.filter(user__username=user.username)
    courses = []
    for enroll in enrolls:
        courses.append(enroll.course)
    teacher = User.objects.filter(username=user.username)
    return render(request, 'teacher/teacher_index.html', {'courses': courses, 'teacher': teacher})


@login_required(login_url='app:login')
def create_homework(request):
    return HttpResponse('create homework')


@login_required(login_url='app:login')
def edit_course(request):
    return HttpResponse('edit course')


@login_required(login_url='app:login')
def edit_homework(request):
    return HttpResponse('edit homework')


@login_required(login_url='app:login')
def course_info(request):
    course_id = request.GET.get('course_id', None)
    if course_id is None:
        return HttpResponse('course_id=None')
    course = Course.objects.filter(id=course_id)
    user = request.user
    enrolls=Enroll.objects.filter(course_id=course_id)
    teachers=[]
    for enroll in enrolls:
        teachers.append(enroll.user)
    teacher = User.objects.filter(username=user.username)
    return render(request, 'teacher/course_info.html', {'course': course, 'teachers': teachers,'teacher':teacher})
