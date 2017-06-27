from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.forms import *


# 在需要鉴别用户身份的地方，调用request.user.is_authenticated()判断即可
# 需要用户登录才能访问的页面，请添加header @login_required(login_url='app:login'),参见test
@login_required(login_url='app:login')
def test(request):
    return HttpResponse('Test page')


# common login page
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'login.html', {'form': form, 'error_message': '用户名或密码不正确'})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('/index')
            else:
                return HttpResponse('您的账户已被禁用')
        else:
            return render(request, 'login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, })


def logout(request):
        auth_logout(request)
        return render(request, 'logout.html')


# Added by kahsolt
def sampleDBView(request):
    from app.utils.sampleDB import sampleDB
    sampleDB()
    return render(request, 'test/sampleDB.html')