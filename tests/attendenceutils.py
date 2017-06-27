from app.models import *
from datetime import datetime


def showBetweenTime(startTime, endTime):
    if not isinstance(startTime, datetime) or not isinstance(endTime, datetime):
        return False, '参数对象错误'

    attendences = Attendance.objects.filter(time__range=(startTime, endTime))
    return attendences


def addAttendance(user):
    if not isinstance(user, User):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'

    attendence = Attendance()
    attendence.user = user
    attendence.save()
    return attendence
