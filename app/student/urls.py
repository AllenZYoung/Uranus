from django.conf.urls import url

from . import views

app_name = 'student'
urlpatterns = [
    url(r'^$', views.index, name='index'), # 学生登录进系统后的“首页”，还没确定放什么内容
    url(r'^member_evaluation$', views.member_evaluation, name='member_evaluation'), # 团队负责人的团队成员评价页面，可设置贡献度等
    url(r'^work_submit$',views.work_submit, name='work_submit'), # 团队负责人的作业提交页面
    url(r'^resources$', views.view_resources, name='resources'),  # 资源列表页面
    url(r'^s', views.download, name='download'),  # 资源下载链接
    url(r'^works', views.view_admitted_work, name='admitted_work'),  # 资源下载链接
    url(r'^work', views.workView, name='work'),  # 资源下载链接
]