from django.shortcuts import render,render_to_response
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from app.models import File, User, Work, WorkMeta, Attachment
from django.conf import settings
import os
from .forms import ContributionForm, UploadFileForm
from .models import Member, User, Team
from django.shortcuts import get_object_or_404
from . import utils
from .utils import *
from .models import Course, Enroll, User
from  django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required(login_url='app:login')
def index(request):  # 也可以看做是“courseRoot函数”
    return render(request, 'student/student_course.html')


@login_required(login_url='app:login')  # 显示学生的课程信息
def my_course(request):
    course_id = request.GET.get('course_id', None)
    if course_id is None:
        print('course_id=None')
    student = request.user
    enroll = Enroll.objects.filter(user__username__contains=student).first()
    course = enroll.course
    print(course)
    return render(request, 'student/student_course_info.html', {'course': course})


# todo 该函数很不完善
@login_required(login_url='app:login')
def member_evaluation(request):  # （团队负责人）学生的团队管理，即成员评价页面
    student_id = request.user
    student = User.objects.filter(username=student_id).first()
    member_model = Member.objects.filter(user__username__contains=student_id).first()
    team = member_model.team

    if request.method == 'GET':  # 显示所有成员及其贡献度（包括队长自己）
        form = UploadFileForm()
        # student_id = request.user
        # member_model = Member.objects.filter(user__username__contains=student_id).first()
        # team = member_model.team
        member_list = Member.objects.filter(team=team)
        return render(request, ''
                               'student/student_team_manage.html',
                      {'team': team, 'member_list': member_list,'form':form})

    elif request.method == 'POST' : # 设置贡献度（权重）
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is VALID!")
            if request.FILES['file'].name.split('.')[-1] == 'xlsx':
                try:
                    handle_uploaded_contribution(request, f=request.FILES['file'])
                except ObjectDoesNotExist as e:
                    error_message = "XLS obeject not exists"
                    return HttpResponse('error')
                return render(request, 'student/student_team_manage.html', {'form': form})
            else:
                error_message = '文件格式错误，请上传Excel文件（.xlsl)'
                form = UploadFileForm()
                return HttpResponse("Your submit is GG")
                # return render(request, 'student/student_team_manage.html', {'form': form, 'errorMessage': error_message})
        else:
            error_message = '请添加文件'
            form = UploadFileForm()
            return HttpResponse("Your submit is GG")
            # return render_to_response('student/student_team_manage.html', {'form': form, 'errorMessage': error_message})
    form = UploadFileForm()
    return render(request, 'student/student_team_manage.html', {'form': form})


def work_submit(request):  # （团队负责人）学生的作业提交页面
    course_id = request.GET.get('course_id', None)

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
    return render(request, 'student/student_course_resources.html', {'file_meta': file_meta, })


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
def view_submitted_work(request):
    team_id = 1
    course_id = 1
    print(1)
    submittings = utils.get_submittings(team_id, course_id)
    print(submittings)
    return render(request, 'student/student_task_view.html', {'submitted': submittings['submitted'], })


# @login_required(login_url='app:login')
def view_unsubmitted_work(request):
    team_id = 1
    course_id = 1
    submittings = utils.get_submittings(team_id, course_id)
    print(submittings)
    return render(request, 'student/student_task_submit.html', {'unsubmitted': submittings['unsubmitted'], })


# added by wanggd 2017-06-28
# @login_required(login_url='app:login')
def workView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ret = utils.submit_homework_file(request)
            if ret:
                return HttpResponse('Sumbit successfully')
            else:
                return HttpResponse('Sumbit failed')
        else:
            return HttpResponse('form is not valid')
    elif request.method == 'GET':
        form = UploadFileForm()
        if 'work_id' in request.GET:
            wid = request.GET['work_id']
            work = Work.objects.get(id=wid)
            files = Attachment.objects.filter(workMeta_id=work.workMeta_id)
            return render(request, 'student/work.html', {'work': work,
                                                         'workMeta': work.workMeta,
                                                         'files': files,
                                                         'is_work': True,
                                                         'form': form})
        else:
            wid = request.GET['workmeta_id']
            workMeta = WorkMeta.objects.get(id=wid)
            return render(request, 'student/work.html', {'workMeta': workMeta,
                                                         'is_work': False,
                                                         'form': form})
    else:
        return HttpResponse('404 NOT FOUND')


# pass
# return render(request,'student/student_task_details.html')


# @login_required(login_url='app:login')

def workRoot(request):
    return render(request, 'student/student_task.html')


def teamRoot(request):
    return render(request, 'student/student_team.html')
