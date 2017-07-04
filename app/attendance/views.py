from django.http import HttpResponse, JsonResponse
from app.utils import *
from django.shortcuts import render, redirect
import os

data = {'start_time': None,
        'end_time': None,
        'is_ended': True,
        'is_started': False,
        'is_collected': False}

# 签到
# TODO: not safe, just make it work!
def attendance(request):
    sid = request.GET.get('id')
    if sid is not None:
        user = User.objects.filter(username=sid).first()
        if addAttendance(user):
            log('(签到)' + user.username, 'attendance', LOG_LEVEL.INFO)
            return HttpResponse('True')
        else:
            return HttpResponse('False')

def attendance_view(request):
    action_id = request.GET.get('action')
    if not action_id:
        data['start_time'] = request.GET.get('start_time')
        data['end_time'] = request.GET.get('end_time')
        data['is_ended'] = False
        data['is_started'] = True
    elif action_id == '1': # 结束签到
        data['is_ended'] = True
        data['is_started'] = False
    elif action_id == '2': # 收集照片
        data['is_collected'] = True
    elif action_id == '3': # 停止收集
        data['is_collected'] = False
    elif action_id == '4': # 向客户端发送数据
        log(data, 'attendance_view')
        log(action_id, 'attendance_view')
        return JsonResponse(data.copy())
    log(data, 'attendance_view')
    log(action_id, 'attendance_view')
    return render(request, 'teacher_collect.html', {'data': data})