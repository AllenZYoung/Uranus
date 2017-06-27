from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import *
from app.teacher.forms import *
from app.teacher.utils import *
from django.shortcuts import get_object_or_404
from app.teacher.entities import *


# Create your views here.
@login_required(login_url='app:login')
def index(request):
    user = request.user
    enrolls = Enroll.objects.filter(user__username=user.username, user__role='teacher')
    course = None
    present = datetime.now()
    for enroll in enrolls:
        if enroll.course.startTime <= present and enroll.course.endTime >= present:
            course = enroll.course
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/teacher_index.html', {'teacher': teacher, 'course': course})


@login_required(login_url='app:login')
def create_homework(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        homework_form = HomeworkForm()
        return render(request, 'teacher/create_homework.html', {'homework_form': homework_form, 'course': course})
    else:
        course_id = request.POST.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        form = HomeworkForm(request.POST)
        if form.is_valid():
            add_homework(form, course_id, request.user.username)
            return HttpResponseRedirect('/homework/')
        else:
            error_message = '数据不合法'
            return render(request, 'teacher/create_homework.html',
                          {'homework_form': form, 'course': course, 'error_message': error_message})


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


@login_required(login_url='app:login')
def resources(request):
    course_id = request.GET.get('course_id', None)
    if course_id is None:
        return HttpResponse('course_id=None')
    course = Course.objects.get(id=course_id)
    user = request.user
    teacher = User.objects.get(username=user.username)
    files = File.objects.filter(course_id=course_id)
    return render(request, 'teacher/resources.html',
                  {'course': course, 'teacher': teacher, 'files': files})


@login_required(login_url='app:login')
def create_resource(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id', None)
        if course_id is None:
            return HttpResponse('course_id=None')
        course = Course.objects.get(id=course_id)
        user = request.user
        upload_file_form = UploadFileForm()
        teacher = User.objects.get(username=user.username)
        return render(request, 'teacher/create_resource.html',
                      {'course': course, 'teacher': teacher, 'upload_file_form': upload_file_form})
    else:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request)
            return HttpResponse('upload file success')
        else:
            return HttpResponse('form is not valid')


@login_required(login_url='app:login')
def homework(request):
    course_id = request.GET.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    works = WorkMeta.objects.filter(course_id=course_id)
    homeworks = []
    for work in works:
        attachments = Attachment.objects.filter(workMeta_id=work.id, type='workmeta')
        homeworks.append(Homework(work, attachments))
    return render(request, 'teacher/homework.html', {'homeworks': homeworks, 'course': course})


# 在线预览课程资源
# @login_required(login_url='app:login')
def preview_source_online(request):
    pass
    # return render(request, 'teacher/sourcePreview.html')


# 设置分数和评论
def add_comment_score(request):
    if request.method == 'GET':
        homework_id = request.GET.get('homework_id')
        homework = get_object_or_404(Work, id=homework_id)
        form = CommentAndScoreForm()
        form.initial['homework_id'] = homework_id
        form.fields['homework_id'].widget = forms.HiddenInput()
        return render(request, 'teacher/add_comment_score.html',
                      {'homework': homework, 'form': form})
    else:
        form = CommentAndScoreForm(request.POST)
        if form.is_valid():
            homework = models.Work.objects.filter(pk=form.cleaned_data['homework_id']) \
                .update(comment=form.cleaned_data['comment'], score=form.cleaned_data['score'])
        else:
            return HttpResponse('fail to add comment and score')


@login_required(login_url='app:login')
def delete_file(request):
    file_id = request.GET.get("file_id", None)
    if file_id is None:
        return HttpResponse('file_id is None')
    File.objects.get(id=file_id).delete()
    return HttpResponse('delete file success')


@login_required(login_url='app:login')
def edit_homework(request):
    if request.method == 'GET':
        workmeta_id = request.GET.get('workmeta_id', None)
        workmeta = get_object_or_404(WorkMeta, id=workmeta_id)
        homework_form = HomeworkForm(content=workmeta.content, proportion=workmeta.proportion, submits=workmeta.submits,
                                     startTime=workmeta.startTime, endTime=workmeta.endTime)
        return render(request, 'teacher/edit_homework.html',
                      {'workmeta_id': workmeta_id, 'homework_form': homework_form})
    else:
        workmeta_id = request.POST.get('workmeta_id', None)
        workmeta = get_object_or_404(WorkMeta, id=workmeta_id)
        homework_form = HomeworkForm(request.POST)
        if homework_form.is_valid():
            workmeta.content = homework_form.cleaned_data['content']
            workmeta.proportion = homework_form.cleaned_data['proportion']
            workmeta.submits = homework_form.cleaned_data['submits']
            workmeta.startTime = homework_form.cleaned_data['startTime']
            workmeta.endTime = homework_form.cleaned_data['endTime']
            workmeta.save()
            return HttpResponse('edit homework success')
        else:
            error_message = '数据不合法'
            return render(request, 'teacher/edit_homework.html',
                          {'workmeta_id': workmeta_id, 'homework_form': homework_form, 'error_message': error_message})


@login_required(login_url='app:login')
def past_homeworks(request):
    user = request.user
    workmetas=get_past_homeworks(user.username)
    return render(request,'teacher/past_homeworks.html',{'workmetas':workmetas})


# 下载学生作业
def download_stu_homework(request):
    pass


# 设置作业占分比例
def set_rate_of_homework(request):
    pass


# 生成个人得分表
def generate_stu_score_table(request):
    pass


# 生成小组最终成绩
def generate_group_score_table(request):
    pass
