from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from app.models import File, User, Work, WorkMeta, Attachment
from django.conf import settings
import os
from .forms import ContributionForm, UploadFileForm
from .models import Member, User, Team
from django.shortcuts import get_object_or_404
from . import utils


# Create your views here.

@login_required(login_url='app:login')
def index(request):
    return render(request, 'student/course_student.html')

# todo 该函数很不完善
@login_required(login_url='app:login')
def member_evaluation(request):  # （团队负责人）学生的团队管理，即成员评价页面
    pass


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
def view_submitted_work(request):
    team_id = 1
    course_id = 1
    print(1)
    submittings = utils.get_submittings(team_id, course_id)
    print(submittings)
    return render(request, 'student/submitted_work.html', {'submitted': submittings['submitted'], })

# @login_required(login_url='app:login')
def view_unsubmitted_work(request):
    team_id = 1
    course_id = 1
    submittings = utils.get_submittings(team_id, course_id)
    print(submittings)
    return render(request, 'student/unsubmitted_work.html', {'unsubmitted': submittings['unsubmitted'], })


# added by wanggd 2017-06-28
#@login_required(login_url='app:login')
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
