from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404
from app.models import *
from app.teacher.forms import *
from app.teacher.utils import *
from django.shortcuts import get_object_or_404
from app.teacher.entities import *
from django.conf import settings


# Create your views here.
@login_required(login_url='app:login')
def index(request):
    user = request.user
    enrolls = Enroll.objects.filter(user__username=user.username, user__role='teacher')
    course = None
    present = datetime.now()
    for enroll in enrolls:
        if enroll.course.startTime.replace(tzinfo=None) <= present <= enroll.course.endTime.replace(tzinfo=None):
            course = enroll.course
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/index.html', {'teacher': teacher, 'course': course})


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
            file=request.FILES['attachment']
            add_homework(form, course_id, request.user.username,file)
            return HttpResponseRedirect('/teacher/homework?course_id='+course_id)
        else:
            error_message = '数据不合法'
            return render(request, 'teacher/create_homework.html',
                          {'homework_form': form, 'course': course, 'error_message': error_message})


@login_required(login_url='app:login')
def edit_course(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        form=EditCourseForm()
        form.set_init_data(course)
        return render(request,'teacher/edit_course.html',{'form':form,'course':course})
    else:
        course_id=request.POST.get('course_id',None)
        course = get_object_or_404(Course, id=course_id)
        form = EditCourseForm(request.POST)
        if form.is_valid():
            course.name=form.cleaned_data['name']
            course.info=form.cleaned_data['info']
            course.syllabus=form.cleaned_data['syllabus']
            course.classroom=form.cleaned_data['classroom']
            course.status=form.cleaned_data['status']
            course.save()
            return redirect('/teacher/course_info?course_id='+course_id)
        else:
            return render(request,'teacher/edit_course.html',{'form':form,'course':course,'error_message':'数据不合法!'})


@login_required(login_url='app:login')
def course_info(request):
    course_id = request.GET.get('course_id', None)
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
        teacher = User.objects.get(username=user.username)
        return render(request, 'teacher/create_resource.html',
                      {'course': course, 'teacher': teacher,})
    else:
        # course_id = request.POST.get('course_id', None)
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     handle_uploaded_file(request,course_id,form)
        #     return HttpResponse('upload file success')
        # else:
        #     return HttpResponse('form is not valid')
        course_id=request.POST.get('course_id',None)
        course=get_object_or_404(Course,id=course_id)
        user = request.user
        teacher = User.objects.get(username=user.username)
        try:
            file = request.FILES['file']
        except:
            return render(request, 'teacher/create_resource.html',
                          {'course': course, 'teacher': teacher, 'error_message': '文件为空!'})
        if file is None:
            return render(request, 'teacher/create_resource.html',
                      {'course': course, 'teacher': teacher,'error_message':'文件为空!'})
        else:
            handle_uploaded_file(request, course_id, file)
            return redirect('/teacher/resources?course_id='+course_id)


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




@login_required(login_url='app:login')
def delete_file(request):
    file_id = request.GET.get("file_id", None)
    course_id=request.GET.get('course_id',None)
    course=get_object_or_404(Course,id=course_id)
    file=get_object_or_404(File,id=file_id)
    location=os.path.join(settings.MEDIA_ROOT,file.file.path)
    if os.path.isfile(location):
        os.remove(location)
    file.delete()
    return redirect('/teacher/resources/?course_id='+course_id)


@login_required(login_url='app:login')
def edit_homework(request):
    if request.method == 'GET':
        workmeta_id = request.GET.get('workmeta_id', None)
        workmeta = get_object_or_404(WorkMeta, id=workmeta_id)
        homework_form = HomeworkForm()
        homework_form.set_data(workmeta)
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
    if len(workmetas) == 0:
        error_message = '当前没有往期作业数据'
    return render(request,'teacher/past_homeworks.html',{'workmetas':workmetas,'error_message':error_message})



# 下载学生作业
def download_stu_homework(request):
    pass



# 生成个人得分表
def generate_stu_score_table(request):
    member_score_dict = compute_member_score()
    stu_list = get_members_list_in_now_term()

    #第一次计算出每个学生的得分后保存到excel表，以便老师下载
    file = get_stu_score_excel_file_abspath()
    if not os.path.isfile(file):
        create_team_score_excel(file, stu_list, member_score_dict)
    return render(request, 'teacher/member_score_list.html',
                  {'member_score_dict': member_score_dict, 'stu_list': stu_list})



#生成小组最终成绩
@login_required(login_url='app:login')
def generate_team_score_table(request):
    team_list, score_list, team_score = compute_team_score()

    # 第一次计算出各团队得分之后保存到excel表，以便老师下载
    file = get_team_score_excel_file_abspath()
    if not os.path.isfile(file):
        create_team_score_excel(file, team_list, team_score)

    return render(request, 'teacher/team_score_list.html',
                  {'team_list': team_list, 'score_list': score_list})


#下载小组得分excel
@login_required(login_url='app:login')
def download_team_score_list():
    file = get_team_score_excel_file_abspath()
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response


# 下载所有学生的分数excel
@login_required(login_url='app:login')
def download_stu_score_list(request):
    file = get_stu_score_excel_file_abspath()
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response


#显示当前已布置的作业
@login_required(login_url='app:login')
def show_works(request):
    course_id = request.GET.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    workmetas=WorkMeta.objects.filter(course_id=course_id)
    # works=[]
    # for workmeta in workmetas:
    #     works.extend(Work.objects.filter(workMeta=workmeta))
    return render(request,'teacher/show_works.html',
                  {'course':course, 'work_metas': workmetas, 'course_id': course_id})


#显示学生提交的一次作业
@login_required(login_url='app:login')
def work_detail(request):
    work_id=request.GET.get('work_id',None)
    work=get_object_or_404(Work,id=work_id)
    attachments=Attachment.objects.filter(workMeta_id=work.workMeta_id)
    return render(request,'teacher/work_detail.html',{'work':work,'attachments':attachments})


#下载上传的资源
@login_required(login_url='app:login')
def download_file(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404



def course(request):
    user = request.user
    enrolls = Enroll.objects.filter(user__username=user.username, user__role='teacher')
    course = None
    present = datetime.now()
    for enroll in enrolls:
        if enroll.course.startTime.replace(tzinfo=None) <= present <= enroll.course.endTime.replace(tzinfo=None):
            course = enroll.course
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/course.html', {'teacher': teacher, 'course': course})


def postcourse(request):
    pass


def task(request):
    course_id=request.GET.get('course_id',None)
    course=get_object_or_404(Course,id=course_id)
    user = request.user
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/task.html', {'teacher': teacher, 'course': course})

# 某作业的所有提交的附件
@login_required(login_url='app:login')
def submitted_work_list(request):
    course_id = request.GET.get('course_id')
    work_meta_id = request.GET.get('work_meta_id')
    workmetas = WorkMeta.objects.filter(id=work_meta_id)
    works=[]
    for workmeta in workmetas:
        works.extend(Work.objects.filter(workMeta=workmeta))
    attachment_team_dict = {}
    for work in works:
        attachments = Attachment.objects.filter(work=work)
        if attachments:
            attachment_team_dict[work.team] = attachments
    return render(request,'teacher/submitted_work_list.html',
                  {'works': works, 'attachment_team_dict': attachment_team_dict, 'work_meta_id': work_meta_id})


# 设置分数和评论
@login_required(login_url='app:login')
def add_comment_score(request):
    if request.method == 'GET':
        work_meta_id = request.GET.get('work_meta_id')
        homework_id = request.GET.get('work_id')
        homework = get_object_or_404(Work, id=homework_id)
        attachments = Attachment.objects.filter(workMeta_id=homework.workMeta_id)
        form = CommentAndScoreForm()
        # form.initial['homework_id'] = homework_id
        # form.fields['homework_id'].widget = forms.HiddenInput()
        # form.initial['post_work_meta_id'] = work_meta_id
        # form.fields['post_work_meta_id'].widget = forms.HiddenInput()
        return render(request, 'teacher/add_comment_score.html',
                      {'homework': homework, 'form': form, 'work_meta_id': work_meta_id,
                       'attachments': attachments})
    else:
        form = CommentAndScoreForm(request.POST)
        work_meta_id = request.GET.get('work_meta_id')
        homework_id = request.GET.get('work_id')
        if form.is_valid():
            homework = Work.objects.filter(pk=homework_id) \
                .update(review=form.cleaned_data['review'], score=form.cleaned_data['score'])
            return redirect('/teacher/submitted_work_list?work_meta_id='+work_meta_id)
        else:
            return HttpResponse('fail to add comment and score!')

