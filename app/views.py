import os

from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from app.forms import *
from app.models import *
from app.utils import *
import json

# 在需要鉴别用户身份的地方，调用request.user.is_authenticated()判断即可
# 需要用户登录才能访问的页面，请添加header @login_required(login_url='app:login'),参见test
@login_required(login_url='app:login')
def test(request):
    return HttpResponse('Test page')


@login_required(login_url='app:login')
def index(request):
    user = get_object_or_404(User, username=request.user.username)
    if user.role == 'student':
        return redirect('/student/')
    elif user.role == 'teacher':
        return redirect('/teacher/')
    else:
        return redirect('/system/')


# common login page
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            data = {}
            data['error_message'] = '用户名或密码错误'
            return HttpResponse(json.dumps(data))
            # return render(request, 'login.html', {'form': form, 'error_message': '用户名或密码不正确'})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        data = {}
        if user:
            if user.is_active:
                auth_login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                else:
                    user=get_object_or_404(User,username=request.user.username)
                    log(user.name or user.username + '登录成功', 'index_login', LOG_LEVEL.INFO)

                    if user.role == 'student':
                        data['user_role'] = 'student'
                    elif user.role == 'teacher':
                        data['user_role'] = 'teacher'
                    else:
                        data['user_role'] = 'system'
            else:
                data['error_message'] = '您的账户已被禁用'
        else:
            data['error_message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(data))

            # return render(request, 'login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, })


def logout(request):
    auth_logout(request)
    return redirect('/user/login')


@login_required(login_url='app:login')
def profile(request):
    user=get_object_or_404(User,username=request.user.username)
    return render(request,'profile.html',{'user':user})


@login_required(login_url='app:login')
def change_info(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'GET':
        form=UserChangeForm()
        form.fields['tel'].initial=user.tel
        form.fields['email'].initial = user.email
        form.fields['desc'].initial = user.desc
        return render(request,'change_info.html',{'form':form,'user':user})
    else:
        form=UserChangeForm(request.POST)
        if form.is_valid():
            tel=form.cleaned_data['tel']
            email=form.cleaned_data['email']
            desc=form.cleaned_data['desc']
            passwd=form.cleaned_data['passwd']
            second_passwd=form.cleaned_data['second_passwd']
            if passwd is not None and passwd != second_passwd:
                return render(request, 'change_info.html', {'form': form, 'error_message': '两次密码输入不一致!'})
            user=get_object_or_404(User,username=request.user.username)
            if tel is not None:
                user.tel=tel
            if email is not None:
                user.email=email
            if desc is not None:
                user.desc=desc
            if passwd is not None and len(passwd) > 0:
                user.password=passwd
                request.user.set_password(passwd)
                request.user.save()
            user.save()
            return redirect('/user/profile')
        else:
            return render(request,'change_info.html',{'form':form,'error_message':'请输入合法数据','user':user})


def bad_request(request):
    return render(request,'pages-error-404.html',status=404)

