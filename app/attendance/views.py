from django.http import HttpResponse
from app.utils import *

# 签到
def attendance(request):
    sid = request.GET.get('id')
    if sid is not None:
        log('(签到)' + sid, 'attendance', LOG_LEVEL.INFO)
        return HttpResponse('Attendance Test')