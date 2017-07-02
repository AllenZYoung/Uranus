from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.utils import *

def index(request):
    return redirect('/user/login')


def log(request):
    logs = []
    with open(LOG_FILE, 'r+') as log:
        for l in log.readlines():
            logs.append(l)
    logs = logs[-100:]
    logs.reverse()
    return render(request, 'log.html', {'logs': logs})


def test(request):
    from app.utils import reportUtils
    reportUtils.test()
    return HttpResponse('Test Finished<br/><a href="/log">See Log</a>')