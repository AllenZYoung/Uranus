# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from app import models
from app.models import Work, WorkMeta
from django.shortcuts import get_object_or_404
from .models import User,Team, TeamMeta, Member
import datetime
import pytz


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


def submit_homework_file(form):  # 提交某个作业（的文件）
    pass

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
