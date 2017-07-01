from django.http import HttpResponse
from app.utils import *

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