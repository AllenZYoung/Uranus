from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import *
from app.teacher.forms import *
from app.teacher.utils import *
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required(login_url='app:login')
def index(request):
    user = request.user
    # 教师首页默认显示该教师的所有课程
    enrolls = Enroll.objects.filter(user__username=user.username, user__role='teacher')
    courses = []
    for enroll in enrolls:
        courses.append(enroll.course)
    teacher = User.objects.get(username=user.username)
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
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    enrolls = Enroll.objects.filter(course_id=course_id)
    teachers = []
    students = []
    for enroll in enrolls:
        if enroll.user.role == 'student':
            students.append(enroll.user)
        elif enroll.user.role == 'teacher':
            teachers.append(enroll.user)
    teacher = get_object_or_404(User, username=user.username)
    import_student_form = UploadFileForm()
    return render(request, 'teacher/course_info.html',
                  {'course': course, 'teachers': teachers, 'teacher': teacher,
                   'students': students, 'import_student_form': import_student_form})


@login_required(login_url='app:login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request)
            return HttpResponse('upload file success')
        else:
            return HttpResponse('form is not valid')
    else:
        return HttpResponse('upload file is empty!')


@login_required(login_url='app:login')
def import_student(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ret = import_student_for_course(request)
            return HttpResponse(ret)
        else:
            return HttpResponse('form is not valid')
    else:
        return HttpResponse('upload file is empty!')


# todo select all resourses for a course
@login_required(login_url='app:login')
def resources(request):
    course_id = request.GET.get('course_id', None)
    if course_id is None:
        return HttpResponse('course_id=None')
    course = Course.objects.get(id=course_id)
    user = request.user
    upload_file_form = UploadFileForm()
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/resources.html',
                  {'course': course, 'teacher': teacher, 'upload_file_form': upload_file_form})


@login_required(login_url='app:login')
def homework(request):
    return HttpResponse('homework')
