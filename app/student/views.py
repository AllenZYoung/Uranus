from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from app.models import File, User, Work, WorkMeta
from django.conf import settings
import os
from .forms import ContributionForm
from .models import Member, User, Team
from django.shortcuts import get_object_or_404
from . import utils


# from .utils import set_members_evaluations


# Create your views here.

@login_required(login_url='app:login')
def index(request):
    return render(request, 'student/course_student.html')


'''
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
                          {'homework_form': form, 'course': course, 'error_message': error_message})'''


# todo 该函数很不完善
@login_required(login_url='app:login')
def member_evaluation(request):  # （团队负责人）学生的团队管理，即成员评价页面
    if request.method == 'GET':  # 显示所有成员及其贡献度（包括队长自己）
        student_id = request.user
        member_model = Member.objects.filter(user__username__contains=student_id).first()
        team = member_model.team
        member_list = Member.objects.filter(team=team)
        contribution_form = ContributionForm()
        return render(request, ''
                               'student/student_member_contribution.html',
                      {'contribution_form': contribution_form, 'team': team, 'member_list': member_list})
    elif request.method == 'POST':  # 改变每个人的权重（贡献度）
        student_id = request.POST.get('name', None)
        f = ContributionForm(request.POST)
        # 此处表单没写好，注意。@果冻
        if f.is_valid():
            # set_members_evaluations(student_id)
            member_model = Member.objects.filter(user__username__contains=student_id)
            team = Team.objects.filter(member_model.team).first()
            member_list = Member.objects.filter(team=team)
            for member in member_list:
                if member.user == f.cleaned_data['user']:
                    member.contribution = f.cleaned_data['contribution']
                    member.save()
        else:
            error_message = 'Some error here!'
            return render(request, 'student/student_member_contribution.html',
                          {'contribution_form': contribution_form, 'error_message': error_message})


# @login_required(login_url='app:login')
def work_submit(request):  # （团队负责人）学生的作业提交页面
    return HttpResponse('Submit your group\'s homework here.')


# @login_required(login_url='app:login')
def view_resources(request):
    files = File.objects.all()
    file_meta = []
    for file in files:
        user = User.objects.get(id=file.user_id)
        file_meta.append({'file_name': file.file,
                          'user_name': user.name,
                          'date': file.time})
    return render(request, 'student/resources.html', {'file_meta': file_meta, })


# @login_required(login_url='app:login')
def download(request):
    def read_file(fn, buf_size=262144):
        f = open(fn, 'rb')
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    file_name = os.path.basename(request.path)
    file_path = os.path.join(settings.MEDIA_ROOT, 'file', file_name)
    response = StreamingHttpResponse(read_file(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


# @login_required(login_url='app:login')
def view_admitted_work(request):
    team_id = 1
    course_id = 1
    submittings = utils.get_submittings(team_id, course_id)
    return render(request, 'student/admitted_work.html', {'submitted': submittings['submitted'],
                                                          'unsubmitted': submittings['unsubmitted'], })


# Added by kahsolt 2017-06-27
# @login_required(login_url='app:login')
def workView(request):
    wid = request.content_params.get('id')
    work = Work.objects.filter(id=wid)
    return render(request, 'student/work.html', {'work': work, })
