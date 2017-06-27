from django.conf.urls import url

from . import views
#TODO 果冻请把所有（子）页面都标注在这里
app_name = 'student'
urlpatterns = [
    url(r'^$', views.index, name='index'), # 学生登录进系统后的“首页”，还没确定放什么内容
    url(r'^member_evaluation$', views.member_evaluation, name='member_evaluation'), # 团队负责人的团队成员评价页面，可设置贡献度等
    url(r'^work_submit$',views.work_submit, name='work_submit'), # 团队负责人的作业提交页面
]