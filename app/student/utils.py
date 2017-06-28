# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from app import models
from app.models import Work, WorkMeta,Member,Team,User
from django.shortcuts import get_object_or_404
from .models import User,Team, TeamMeta, Member, File, Attachment
from django.conf import settings
import datetime
import pytz
import os
from openpyxl.reader.excel import load_workbook
from ..utils.teamUtils import setContribution, isTeamLeader



def auth_user(form):  # 瞎写的东西
    if form.is_valid():
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        # check
        user = models.User.objects.filter(username=username, password=password)
        if user:
            return True
        else:
            return False
    else:
        return False

# 提交某个作业（的文件），只能是负责人提交
def submit_homework_file(request):
    team_id = course_id = user_id = team_id = workMeta_id = 1
    f = request.FILES['file']
    upload_path = os.path.join(settings.MEDIA_ROOT, 'file\student', f.name)
    with open(upload_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    file = File(file=f.name, course_id=course_id, user_id=user_id)
    file.save()
    work = Work(team_id=team_id, workMeta_id=workMeta_id)
    work.save()
    Attachment(file_id=file.id, work_id=work.id, workMeta_id=workMeta_id).save()
    return True


#TODO this function, some puzzled questions here
# def set_members_evaluations(team_leader):  # 为团队成员设置贡献度（可以理解为权重）
#     member_model = Member.objects.filter(user__username__contains=team_leader)
#     team = Team.objects.filter(member_model.team).first()
#     member_list = Member.objects.filter(team=team)
#     for member in member_list:
#         member.contribution =


# 获得对应团队，对应课程的提交情况，包括已提交和未提交
def get_submittings(team_id, course_id):

    submittings = {'submitted': [], 'unsubmitted': []}
    # 选择最晚提交作业
    last_submit = {}
    for work in Work.objects.filter(team_id=team_id):
        if work.workMeta_id not in last_submit:
            last_submit[work.workMeta_id] = {'work': work,
                                             'time': datetime.datetime(2017, 1, 1, tzinfo=pytz.utc)}
        if work.time > last_submit[work.workMeta_id]['time']:
            last_submit[work.workMeta_id]['time'] = work.time
            last_submit[work.workMeta_id]['work'] = work

    last_submit = sorted(last_submit.items(), key=lambda d: d[0], reverse=False)
    submittings['submitted'] = [item[1]['work'] for item in last_submit]
    submitted_id = [item.workMeta_id for item in submittings['submitted']]

    # 没有提交的作业
    for workMeta in WorkMeta.objects.filter(course_id=course_id):
        if workMeta.id not in submitted_id:
            submittings['unsubmitted'].append(workMeta)
    return submittings

def handle_uploaded_contribution(request, f=None):
    datenow = datetime.datetime.now()
    filedate = datenow.strftime('%Y%m%d-%H%M%S')
    path = os.path.join(os.path.abspath('.'),'uploads','user')
    filepath = path + '/' + filedate + '_' + f.name
    with open(filepath, 'ab') as de:
        for chunk in f.chunks():
            de.write(chunk)
    wb = load_workbook(filepath)
    print(filepath)
    table = wb.get_sheet_by_name(wb.get_sheet_names()[0])
    for i in range(2, table.max_row + 1):
        if table.cell(row=i, column=1).value is None:
            # '为空，应跳过'
            continue
        print('正在导入第' + str(i - 1) + '行...')

        student_id = table.cell(row=i,column=1).value
        student_contribution = table.cell(row=i, column=3).value
        print(student_id, student_contribution)
        student = User.objects.filter(username=student_id).first()
        # if student is not None:
        #     Member.objects.filter(user=student).update(contribution=student_contribution)
        # else:
        #     return None
        setContribution(student,student_contribution)
