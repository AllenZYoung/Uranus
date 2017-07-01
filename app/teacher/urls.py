from django.conf.urls import url
from . import generic_views
from . import views

app_name = 'teacher'
urlpatterns = [
    url(r'^$', views.course, name='index'),
    url(r'^create_homework/', views.create_homework, name='create_homework'),
    url(r'^edit_homework/', views.edit_homework, name='edit_homework'),
    url(r'^course_info/', views.course_info, name='course_info'),
    url(r'^edit_course/', views.edit_course, name='edit_course'),
    url(r'^resources/', views.resources, name='resources'),
    url(r'^create_resource/',views.create_resource,name='create_resource'),
    url(r'^homework/', views.homework, name='homework'),
    url(r'^import_student/', views.import_student, name='import_student'),
    url(r'^add_comment_score/', views.add_comment_score, name='add_comment_score'),
    url(r'^delete_file/',views.delete_file,name='delete_file'),
    url(r'^edit_homework/',views.edit_homework,name='edit_homework'),
    url(r'^past_homeworks/',views.past_homeworks,name='past_homeworks'),
    url(r'^generate_team_score_table$', views.generate_team_score_table, name='generate_team_score_table'),
    url(r'^download_team_score_list$', views.download_team_score_list, name='download_team_score_list'),
    url(r'^generate_stu_score_table$', views.generate_stu_score_table, name='generate_stu_score_table'),
    url(r'^download_stu_score_list$', views.download_stu_score_list, name='download_stu_score_list'),
    url(r'^show_works/',views.show_works,name='show_works'),
    url(r'^work_detail/',views.work_detail,name='work_detail'),
    url(r'^uploads/(?P<path>.*)$',views.download_file,name='download_file'),
    url(r'^course/',views.course,name='course'),
    url(r'^task/',views.task,name='task'),
    url(r'^submitted_work_list/', views.submitted_work_list, name='submitted_work_list'),
    url(r'^preview_source_online/', views.preview_source_online, name='preview_source_online'),
    url(r'^score_manage/',views.score_manage,name='score_manage'),
    url(r'^team_manage/', views.team_manage, name='team_manage'),
    url(r'^teams/',views.teams,name='teams'),
    url(r'^team_members/',views.team_members,name='team_members'),
    url(r'^adjust_team/',views.adjust_team,name='adjust_team'),
    url(r'^dismiss_member/',views.dismiss_member,name='dismiss_member'),

]
