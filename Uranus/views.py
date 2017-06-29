from django.http import HttpResponse
from django.shortcuts import render, redirect

#from app.test.sampleDB import sampleDB



def index(request):
    return redirect('/user/login')


    # str='<h1>Uranus Project</h1>'
    # str+='<br/><div>'
    # str+='<h3>安装样例数据库</h3>'
    # str+='<p style="color: red;">请先以普通py脚本的方式运行/Uranus/META/sampleDB_base.py<br/>'
    # str+='如果数据库崩了请运行/Uranus/META/reinit.sql</p>'
    # str+='<p><a href="test/sampleDB">[[Start Install Sample DB]]</a><p>'
    # str+='</div>'
    # return HttpResponse(str)


# Added by kahsolt
def sampleDBView(request):
   # sampleDB()
    return render(request, 'test/sampleDB.html')


