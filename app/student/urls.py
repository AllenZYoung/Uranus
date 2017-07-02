from django.conf.urls import url

from . import views
from app.attendance.views import attendance

app_name = 'student'
urlpatterns = [
    url(r'^$', views.index, name='index'), # 学生登录进系统后的“首页”，还没确定放什么内容
    url(r'^member_evaluation$', views.member_evaluation, name='member_evaluation'), # 团队负责人的团队成员评价页面，可设置贡献度等
    url(r'^resources$', views.view_resources, name='resources'),  # 资源列表页面
    url(r'^submits$', views.view_submitted_work, name='submitted_work'),  # 查看作业提交情况
    url(r'^unsubmits$', views.view_unsubmitted_work, name='unsubmitted_work'),  # 查看未提交情况
    url(r'^student_team_build$', views.student_team_build ,name='student_team_build'),
    url(r'^s', views.download, name='download'),  # 资源下载链接
    url(r'^workpage$', views.workRoot, name='workpage'),  # 查看作业详情
    url(r'^work', views.workView, name='work'),  # 查看作业详情
    url(r'^teampage$',views.teamRoot, name='teampage') ,# 团队主页，其下有多个功能
    url(r'^mycourse$',views.my_course,name='my_course'),
    url(r'^attendance', attendance),  # 签到
    url(r'^apply_for_team', views.apply_for_team),  # 申请加入团队
    url(r'^process_apply', views.process_apply),  # 处理申请请求
    url(r'^finish_team_bulid', views.finish_team_bulid),  # 处理申请请求
]