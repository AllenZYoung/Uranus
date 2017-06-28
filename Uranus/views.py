from django.http import HttpResponse
from django.shortcuts import render
from app.test.sampleDB import sampleDB


def index(request):
    str='<h1>Uranus Project</h1>'
    str+='<br/><div>'
    str+='<p><a href="test/sampleDB">Install Sample DB</a><p>'
    str+='<p>请先以普通py脚本的方式运行/Uranus/META/sampleDB_base.py</p>'
    str+='<p>如果数据库崩了请运行/Uranus/META/reinit.sql</p>'
    str+='</div>'
    return HttpResponse(str)


# Added by kahsolt
def sampleDBView(request):
    sampleDB()
    return render(request, 'test/sampleDB.html')