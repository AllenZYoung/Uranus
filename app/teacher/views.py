from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404, JsonResponse
from app.models import *
from app.teacher.forms import *
from app.teacher.utils import *
from django.shortcuts import get_object_or_404
from app.teacher.entities import *
from django.conf import settings
from app.templatetags import app_tags
from app.utils import *
import pprint


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
            request.session['course_id'] = course.id
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/index.html', {'teacher': teacher, 'course': course})


@login_required(login_url='app:login')
def create_homework(request):
    if request.method == 'GET':
        course_id = request.session.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        form = HomeworkForm()
        return render(request, 'teacher/create_homework.html', {'form': form, 'course': course})
    else:
        data = {}
        course_id = request.session.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                file = request.FILES['attachment']
            except:
                file = None
            add_homework(form, course_id, request.user.username, file)
            data['success'] = 'true'
            data['forward_url'] = '/teacher/homework?course_id=' + str(course_id)
            # return HttpResponseRedirect('/teacher/homework?course_id=' + str(course_id))
        else:
            data['error_message'] = '数据不合法'
            # return render(request, 'teacher/create_homework.html',
            #               {'form': form, 'course': course, 'error_message': error_message})
        return HttpResponse(json.dumps(data))


@login_required(login_url='app:login')
def edit_course(request):
    if request.method == 'GET':
        course_id = request.session.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        form = EditCourseForm()
        form.set_init_data(course)
        return render(request, 'teacher/edit_course.html', {'form': form, 'course': course})
    else:
        data = {}
        course_id = request.session.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        form = EditCourseForm(request.POST)
        if form.is_valid():
            course.name = form.cleaned_data['name']
            course.info = form.cleaned_data['info']
            course.syllabus = form.cleaned_data['syllabus']
            course.classroom = form.cleaned_data['classroom']
            course.status = form.cleaned_data['status']
            course.save()

            data['success'] = 'true'
            data['forward_url'] = '/teacher/course_info/?course_id=' + str(course_id)

            # return redirect('/teacher/course_info?course_id=' + str(course_id))
        else:
            data['error_message'] = '数据不合法，请重新填写！'
            # return render(request, 'teacher/edit_course.html',
            #               {'form': form, 'course': course, 'error_message': '数据不合法!'})
        return HttpResponse(json.dumps(data))


@login_required(login_url='app:login')
def course_info(request):
    course_id = request.session.get('course_id', None)
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
    course_id = request.session.get('course_id', None)
    if course_id is None:
        return HttpResponse('course_id=None')
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    teacher = User.objects.get(username=user.username)

    files = File.objects.filter(course_id=course_id, user=teacher).order_by('-time')
    return render(request, 'teacher/resources.html',
                  {'course': course, 'teacher': teacher, 'files': files})


@login_required(login_url='app:login')
def create_resource(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'GET':
        return render(request, 'teacher/create_resource.html',
                      {'course': course, })
    else:
        data = {}
        if len(request.FILES.getlist('files')) == 0:
            data['error_message'] = '文件为空，请重新上传！'
            return HttpResponse(json.dumps(data))
        for file in request.FILES.getlist('files'):
            handle_uploaded_file(request, course_id, file)
        data['success'] = 'true'
        data['forward_url'] = '/teacher/resources'
        return HttpResponse(json.dumps(data))


@login_required(login_url='app:login')
def homework(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    works = WorkMeta.objects.filter(course_id=course_id)
    homeworks = []
    for work in works:
        if work.submits != -10:
            attachments = Attachment.objects.filter(workMeta_id=work.id, type='workmeta')
            homeworks.append(Homework(work, attachments))
    return render(request, 'teacher/homework.html', {'homeworks': homeworks, 'course': course})


# 在线预览课程资源
# @login_required(login_url='app:login')
def preview_source_online(request):
    file = request.GET.get('file')
    log('file_path=' + file, 'preview_source_online')
    url = fileUtils.docPreviewUrl(file)
    log(url, 'preview_source_online')
    return redirect(url)


@login_required(login_url='app:login')
def delete_file(request):
    file_id = request.GET.get("file_id", None)
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    file = get_object_or_404(File, id=file_id)
    location = os.path.join(UPLOAD_ROOT, file.file.path)
    if os.path.isfile(location):
        os.remove(location)
    file.delete()
    data = {}
    data['success'] = 'true'
    return HttpResponse(json.dumps(data))
    # return redirect('/teacher/resources/?course_id=' + str(course_id))


@login_required(login_url='app:login')
def edit_homework(request):
    if request.method == 'GET':
        workmeta_id = request.GET.get('workmeta_id', None)
        course_id = request.session.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        workmeta = get_object_or_404(WorkMeta, id=workmeta_id)
        homework_form = HomeworkForm()
        homework_form.set_data(workmeta)
        return render(request, 'teacher/edit_homework.html',
                      {'course': course, 'workmeta_id': workmeta_id, 'form': homework_form})
    else:
        data = {}
        teacher = User.objects.get(username=request.user.username)
        workmeta_id = request.POST.get('workmeta_id', None)
        course_id = request.session.get('course_id', None)
        course = get_object_or_404(Course, id=course_id)
        workmeta = get_object_or_404(WorkMeta, id=workmeta_id)
        homework_form = HomeworkForm(request.POST)
        if homework_form.is_valid():
            workmeta.title = homework_form.cleaned_data['title']
            workmeta.content = homework_form.cleaned_data['content']
            workmeta.proportion = homework_form.cleaned_data['proportion']
            workmeta.submits = homework_form.cleaned_data['submits']
            workmeta.endTime = homework_form.cleaned_data['endTime']
            try:
                file = request.FILES['attachment']
            except:
                file = None
            if file is not None:
                f = File(course=course, user=teacher, file=file, type='text', time=datetime.now())
                f.save()
                attachment = Attachment(file=f, workMeta=workmeta, type='workmeta')
                attachment.save()
            workmeta.save()
            data['success'] = 'true'
            data['forward_url'] = '/teacher/homework/?course_id=' + str(course_id)
            # return redirect('/teacher/homework/?course_id=' + str(course_id))
        else:
            data['error_message'] = '数据不合法'
            # return render(request, 'teacher/edit_homework.html',
            #               {'course': course, 'workmeta_id': workmeta_id, 'form': homework_form,
            #                'error_message': error_message})
        return HttpResponse(json.dumps(data))


@login_required(login_url='app:login')
def past_homeworks(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    workmetas = get_past_homeworks(user.username)
    if len(workmetas) == 0:
        error_message = '当前没有往期作业数据'
    return render(request, 'teacher/past_homeworks.html',
                  {'course': course, 'workmetas': workmetas, 'error_message': error_message})


# 生成个人得分表
@login_required(login_url='app:login')
def generate_stu_score_table(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    stu_score_dict = compute_stu_score()
    stu_list = get_stu_list_in_now_course()
    # 第一次计算出每个学生的得分后保存到excel表，以便老师下载
    file = get_stu_score_excel_file_abspath()
    # if not os.path.isfile(file):
    create_stu_score_excel(file, stu_list, stu_score_dict)
    return render(request, 'teacher/stu_score_list.html',
                  {'stu_score_dict': stu_score_dict, 'stu_list': stu_list, 'course': course})


# 生成小组最终成绩
@login_required(login_url='app:login')
def generate_team_score_table(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    team_list, score_list, team_score = compute_team_score()
    # 第一次计算出各团队得分之后保存到excel表，以便老师下载
    file = get_team_score_excel_file_abspath()
    # if not os.path.isfile(file):
    create_team_score_excel(file, team_list, score_list)
    num_list = range(len(team_list))

    return render(request, 'teacher/team_score_list.html',
                  {'team_list': team_list, 'score_list': score_list, 'num_list': num_list, 'course': course})


# 下载小组得分excel
@login_required(login_url='app:login')
def download_team_score_list(request):
    file = get_team_score_excel_file_abspath()
    if os.path.exists(file):
        response = StreamingHttpResponse(file_iterator(file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + os.path.basename(file)
        return response
    return Http404


# 下载所有学生的分数excel
@login_required(login_url='app:login')
def download_stu_score_list(request):
    file = get_stu_score_excel_file_abspath()
    if os.path.exists(file):
        response = StreamingHttpResponse(file_iterator(file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + os.path.basename(file)
        return response
    return Http404


# 下载所有学生及团队的excel  url:/teacher/download_stu_teams
@login_required(login_url='app:login')
def download_team_members_all(request):
    file = get_team_members_all_excel_file_abspath()
    teacher = request.user
    course = Enroll.objects.filter(user__username__contains=teacher).first().course
    create_stu_teams_excel(file, course)
    if os.path.exists(file):
        response = StreamingHttpResponse(file_iterator(file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + os.path.basename(file)
        return response
    return Http404


# 显示当前已布置的作业
@login_required(login_url='app:login')
def show_works(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    workmetas_raw = WorkMeta.objects.filter(course_id=course_id)
    workmetas = []
    for workmeta in workmetas_raw:
        print(workmeta.endTime)
        if workmeta.submits != -10:
            workmetas.append(workmeta)
    # works=[]
    # for workmeta in workmetas:
    #     works.extend(Work.objects.filter(workMeta=workmeta))
    return render(request, 'teacher/show_works.html',
                  {'course': course, 'work_metas': workmetas, 'course_id': course_id})


# 显示学生提交的一次作业
@login_required(login_url='app:login')
def work_detail(request):
    work_id = request.GET.get('work_id', None)
    work = get_object_or_404(Work, id=work_id)
    attachments = Attachment.objects.filter(workMeta_id=work.workMeta_id)
    return render(request, 'teacher/work_detail.html', {'work': work, 'attachments': attachments})


# 下载上传的资源
@login_required(login_url='app:login')
def download_file(request, path):
    file_path = os.path.join(UPLOAD_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required(login_url='app:login')
def course(request):
    user = request.user
    enrolls = Enroll.objects.filter(user__username=user.username, user__role='teacher')
    course = None
    present = datetime.now()
    course = Enroll.objects.filter(user__username__contains=user).first().course
    notice_new = Notice.objects.filter(course=course).order_by('-time').first()

    for enroll in enrolls:
        if enroll.course.startTime.replace(tzinfo=None) <= present <= enroll.course.endTime.replace(tzinfo=None):
            course = enroll.course
            request.session['course_id'] = course.id
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/course.html', {'teacher': teacher, 'course': course, 'notice': notice_new})


@login_required(login_url='app:login')
def task(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    teacher = User.objects.get(username=user.username)
    return render(request, 'teacher/task.html', {'teacher': teacher, 'course': course})


# 某作业的所有提交的附件
@login_required(login_url='app:login')
def submitted_work_list(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    work_meta_id = request.GET.get('work_meta_id')
    workmeta = WorkMeta.objects.get(id=work_meta_id)
    teams = Team.objects.filter(course=course, status='passed')
    works = []
    for team in teams:
        work = Work.objects.filter(workMeta=workmeta, team=team).order_by('-time').last()
        if work:
            works.append(work)
    attachment_team_dict = {}
    for work in works:
        attachments = Attachment.objects.filter(work=work)
        if attachments:
            attachment_team_dict[work.team] = attachments

    return render(request, 'teacher/submitted_work_list.html',
                  {'works': works, 'attachment_team_dict': attachment_team_dict, 'work_meta_id': work_meta_id, })


# 设置分数和评论
@login_required(login_url='app:login')
def add_comment_score(request):
    work_meta_id = request.GET.get('work_meta_id')
    course_id = request.session.get('course_id', None)
    homework_id = request.GET.get('work_id')
    homework = get_object_or_404(Work, id=homework_id)
    # work_meta = WorkMeta.objects.filter(id=work_meta_id)
    attachments = Attachment.objects.filter(work=homework)
    if request.method == 'GET':
        form = CommentAndScoreForm()
        return render(request, 'teacher/add_comment_score.html',
                      {'homework': homework, 'form': form, 'work_meta_id': work_meta_id,
                       'attachments': attachments})
    else:
        data = {}
        form = CommentAndScoreForm(request.POST)
        work_meta_id = request.GET.get('work_meta_id')
        homework_id = request.GET.get('work_id')
        if form.is_valid():
            homework = Work.objects.filter(pk=homework_id) \
                .update(review=form.cleaned_data['review'], score=form.cleaned_data['score'])
            # return render(request, 'teacher/success.html',
            #               {'name_space': 'teacher', 'forward_url': 'submitted_work_list', 'params': '?work_meta_id='+work_meta_id})
            data['success'] = 'true'
            data['forward_url'] = '/teacher/submitted_work_list?work_meta_id=' + work_meta_id + '&course_id=' + str(
                course_id)

            # return redirect('/teacher/submitted_work_list?work_meta_id=' + work_meta_id + '&course_id=' + str(course_id))
        else:
            data['error_message'] = '数据不合法，请重新填写！'
            # return render(request, 'teacher/add_comment_score.html',
            #               {'homework': homework, 'form': form, 'work_meta_id': work_meta_id,
            #                'attachments': attachments, 'error_message': error_message})
        return HttpResponse(json.dumps(data))


@login_required(login_url='app:login')
def score_manage(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'teacher/score_manage.html', {'course': course})


@login_required(login_url='app:login')
def team_manage(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'teacher/teacher_team_manage.html', {'course': course})


@login_required(login_url='app:login')
def teams(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    teams = Team.objects.filter(course_id=course.id, status='passed')
    unteamed_students = query_unteamed_students(course_id)
    return render(request, 'teacher/show_teams.html',
                  {'course': course, 'unteamed_students': unteamed_students, 'teams': teams})


@login_required(login_url='app:login')
def team_members(request):
    team_id = request.GET.get('team_id', None)
    course_id = request.session.get('course_id', None)
    team = get_object_or_404(Team, id=team_id)
    course = get_object_or_404(Course, id=course_id)
    members = Member.objects.filter(team=team)
    return render(request, 'teacher/team_members.html', {'team': team, 'course': course, 'members': members})


@login_required(login_url='app:login')
def adjust_team(request):
    student_id = request.POST.get('student_id', None)
    course_id = request.session.get('course_id', None)
    student = get_object_or_404(User, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    serial_num = request.POST.get('serial_num' + student.username, None)
    if serial_num is None:
        return HttpResponse('请选择要调整至的队伍')
    team = get_object_or_404(Team, serialNum=serial_num)
    member = Member(team=team, user=student, role='member', contribution=0)
    member.save()
    return redirect('/teacher/teams?student_id=' + student_id)


@login_required(login_url='app:login')
def dismiss_member(request):
    team_id = request.GET.get('team_id', None)
    member_id = request.GET.get('member_id', None)
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('/teacher/team_members?team_id=' + team_id)


@login_required(login_url='app:login')
def team_apply(request):
    course_id = request.session.get('course_id', None)
    course = get_object_or_404(Course, id=course_id)
    teams = Team.objects.filter(course=course, status='auditing')
    return render(request, 'teacher/team_apply.html', {'teams': teams, 'course': course})


@login_required(login_url='app:login')
def apply_manage(request):
    if request.method == 'GET':
        team_id = request.GET.get('team_id', None)
        team = get_object_or_404(Team, id=team_id)
        form = EditTeamForm()
        return render(request, 'teacher/apply_manage.html', {'team': team, 'form': form})
    else:
        team_id = request.POST.get('team_id', None)
        team = get_object_or_404(Team, id=team_id)
        # print(team)
        form = EditTeamForm(request.POST)
        if form.is_valid():
            team.info = form.cleaned_data['info']

            if form.cleaned_data['status'] == 'passed':
                auditTeamPassed(team)
                print("auditTeamPassed done!")
            elif form.cleaned_data['status'] == 'rejected':
                auditTeamRejected(team)
                team.save()
            return redirect('/teacher/team_apply')
        else:
            return render(request, 'teacher/apply_manage.html', {'team': team, 'form': form, 'error_message': '数据不合法'})


# 生成所有团队每次作业的成绩报表
@login_required(login_url='app:login')
def score_report(request):
    course_id = request.session.get('course_id', None)
    scores = generate_team_scores(course_id)
    teams = Team.objects.filter(course_id=course_id, status='passed')
    return render(request, 'teacher/score_report.html', {'datas': scores, 'teams': teams})


# 生成单次作业的成绩报表
@login_required(login_url='app:login')
def single_workmeta_report(request):
    course_id = request.session.get('course_id', None)
    workmeta_id = request.GET.get('workmeta_id', None)
    dest = generate_single_workmeta_exccel(course_id, workmeta_id)
    return download(dest)


@login_required(login_url='app:login')
def generate_score_excel(request):
    course_id = request.session.get('course_id', None)
    dest = generate_scores_excel(course_id)
    return download(dest)


@login_required(login_url='app:login')
def add_score_params(request):
    course_id = request.session.get('course_id', None)
    teams = Team.objects.filter(course_id=course_id, status='passed')
    user = User.objects.get(username=request.user.username)
    if request.method == 'GET':
        form = ScoreParamForm()
        form.add_fields(teams)
        return render(request, 'teacher/add_score_params.html', {'form': form})
    else:
        data = {}
        form = ScoreParamForm(request.POST)
        if form.is_valid():
            workmeta = WorkMeta(course_id=course_id, user=user, title=form.cleaned_data['title'],
                                content=form.cleaned_data['content'],
                                proportion=form.cleaned_data['proportion'], submits=-10, startTime=datetime.now(),
                                endTime=datetime.now())
            workmeta.save()
            for team in teams:
                work = Work(workMeta=workmeta, team=team, score=request.POST.get(str(team.serialNum)),
                            time=datetime.now())
                work.save()
            data['success'] = 'true'
            data['forward_url'] = '/teacher/score_report'
            # return redirect('/teacher/score_report')
        else:
            data['error_message'] = '数据不合法，请重新填写！'
            # return render(request, 'teacher/add_score_params.html', {'form': form,'error_message':'数据不合法!'})
        return HttpResponse(json.dumps(data))


@login_required(login_url='app:login')
def setNotice(request):
    user = request.user
    course = Enroll.objects.filter(user__username__contains=user).first().course
    user = User.objects.filter(username__contains=user).first()
    notices = Notice.objects.filter(course=course).order_by('-time')
    if request.method == 'GET':
        form = NoticeForm()
        return render(request, 'teacher/teacher_course_announcement.html', {'notices': notices, 'form': form})
    elif request.method == 'POST':
        user = request.user
        course = Enroll.objects.filter(user__username__contains=user).first().course
        user = User.objects.filter(username__contains=user).first()
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = Notice(course=course, user=user, title=form.cleaned_data['title'],
                            content=form.cleaned_data['content'])
            notice.save()
            return render(request, 'teacher/teacher_course_announcement.html', {'notices': notices, 'form': form})
        else:
            return HttpResponse('数据不合法，请重新填写！')
    return render(request, 'teacher/teacher_course_announcement.html')


data = {'is_ended': True,
        'is_started': False,
        'is_collected': False}


def attendance_view(request):
    action_id = request.GET.get('action')
    if action_id == '0': # 开始签到
        course_id = request.session.get('course_id', None)
        data['is_ended'] = False
        data['is_started'] = True
        data['is_collected'] = False
        enrolls = Enroll.objects.filter(course_id=course_id)
        attendance = showToday()
        attendance_id = [item.user_id for item in attendance]
        unattendance = [enroll.user for enroll in enrolls if enroll.user_id not in attendance_id]
        return render(request, 'teacher/teacher_check.html', {'data': data,
                                                              'attendance': attendance,
                                                              'unattendance': unattendance, })
    elif action_id == '1' or action_id is None or not action_id or action_id == '': # 结束签到
        course_id = request.session.get('course_id', None)
        data['is_ended'] = True
        data['is_started'] = False
        data['is_collected'] = False
        enrolls = Enroll.objects.filter(course_id=course_id)
        attendance =  showToday()
        attendance_id = [item.user_id for item in attendance]
        unattendance = [enroll.user for enroll in enrolls if enroll.user_id not in attendance_id]
        return render(request, 'teacher/teacher_check.html', {'data': data,
                                                              'attendance': attendance,
                                                              'unattendance': unattendance,})
    elif action_id == '2': # 收集照片
        data['is_collected'] = True
        data['is_started'] = False
        data['is_ended'] = True
        return render(request, 'teacher/teacher_collect.html', {'data': data,})
    elif action_id == '3': # 停止收集
        data['is_collected'] = False
        data['is_started'] = False
        data['is_ended'] = True
        return render(request, 'teacher/teacher_collect.html', {'data': data,})
    elif action_id == '4': # 向客户端发送数据
        return JsonResponse(data.copy())


@login_required(login_url='app:login')
def teacher_attendance(request):
    return render(request, 'teacher/teacher_attendence.html')


@login_required(login_url='app:login')
def teacher_collect(request):
    return render(request, 'teacher/teacher_collect.html', {'data': data})


@login_required(login_url='app:login')
def teacher_check(request):
    course_id = request.session.get('course_id', None)
    enrolls = Enroll.objects.filter(course_id=course_id)
    attendance = showToday()
    attendance_id = [item.user_id for item in attendance]
    unattendance = [enroll.user for enroll in enrolls if enroll.user_id not in attendance_id]
    return render(request, 'teacher/teacher_check.html', {'data': data,
                                                          'attendance': attendance,
                                                          'unattendance': unattendance, })


def test(request):
    if request.method == 'GET':
        return render(request, 'teacher/test.html')
    else:
        name = request.POST.get('name', None)
        data = {}
        data['content'] = 'hello ' + name
        return HttpResponse(json.dumps(data))
