from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from app.models import File, User, Work, WorkMeta
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from . import utils
from .utils import set_members_evaluations
#TODO 学生登录和注销（一般而言，要与教师、教务统一）



# Create your views here.
def index(request):
    return render(request,'student/course_student.html')

#@login_required(login_url='app:login')
def member_evaluation(request): # （团队负责人）学生的成员评价页面
    if request.method == 'GET':
        student_id = request.GET.get('student_id',None)
        student = User.objects.get(username=student_id)
        set_members_evaluations(student)
    return HttpResponse('Member Evaluation here.')

#@login_required(login_url='app:login')
def work_submit(request): # （团队负责人）学生的作业提交页面
    return HttpResponse('Submit your group\'s homework here.')

#@login_required(login_url='app:login')
def view_resources(request):
    files = File.objects.all()
    file_meta = []
    for file in files:
        user = User.objects.get(id=file.user_id)
        file_meta.append({'file_name': file.file,
                          'user_name': user.name,
                          'date': file.time})
    return render(request, 'student/resources.html', {'file_meta': file_meta, })

#@login_required(login_url='app:login')
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

#@login_required(login_url='app:login')
def view_admitted_work(request):
    team_id = 1
    course_id = 1
    submittings = utils.get_submittings(team_id, course_id)
    return render(request, 'student/admitted_work.html', {'submitted': submittings['submitted'],
                                                          'unsubmitted': submittings['unsubmitted'],})


# Added by kahsolt 2017-06-27
#@login_required(login_url='app:login')
def workView(request):
    wid = request.content_params.get('id')
    work = Work.objects.filter(id=wid)
    return render(request, 'student/work.html', {'work': work,})
