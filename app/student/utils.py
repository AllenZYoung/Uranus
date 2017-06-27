# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from app import models
from app.models import Work, WorkMeta

def auth_user(form): # 瞎写的东西
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

def set_members_evaluations(form): # 为团队成员设置贡献度（可以理解为权重）
    pass

# 获得对应团队，对应课程的提交情况，包括已提交和未提交
def get_submittings(team_id, course_id):
    submittings = {'submitted': [], 'unsubmitted': []}
    submitted_id = set()
    # 提交的作业
    for work in Work.objects.filter(team_id=team_id):
        if work.workMeta_id not in submitted_id:
            submittings['submitted'].append(WorkMeta.objects.get(id=work.workMeta_id))
            submitted_id.add(work.workMeta_id)
    # 没有提交的作业
    for workMeta in WorkMeta.objects.filter(course_id=course_id):
        if workMeta.id not in submitted_id:
            submittings['unsubmitted'].append(workMeta)
    return submittings
