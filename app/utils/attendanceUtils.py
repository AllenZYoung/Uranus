from app.utils.logUtils import log, LOG_LEVEL
from datetime import datetime
from app.models import *

# 关于签到的工具集
# by kahsolt


def showToday():
    startTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 0, 0, 0)
    endTime = datetime.now()
    attendances = Attendance.objects.filter(time__range=(startTime, endTime)).order_by('time')
    return attendances


def showTimeBetween(startTime, endTime):
    if not isinstance(startTime, datetime) or not isinstance(endTime, datetime):
        return None

    attendances = Attendance.objects.filter(time__range=(startTime, endTime)).order_by('time')
    return attendances


def addAttendance(user):
    if not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'attendanceUtils', LOG_LEVEL.ERROR)
        return False

    attendence = Attendance()
    attendence.user = user
    attendence.save()
    return attendence
