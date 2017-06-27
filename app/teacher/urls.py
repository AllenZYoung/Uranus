from django.conf.urls import url
from . import generic_views
from . import views

app_name = 'teacher'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_homework/', views.create_homework, name='create_homework'),
    #url(r'^edit_course/', views.edit_course, name='edit_course'),
    url(r'^edit_homework/', views.edit_homework, name='edit_homework'),
    url(r'^course_info/', views.course_info, name='course_info'),
    url(r'^course_edit_form/(?P<pk>[0-9]+)$', generic_views.CourseUpdate.as_view(), name='edit_course'),
    url(r'^resources/', views.resources, name='resources'),
    url(r'create_resource/',views.create_resource,name='create_resource'),
    url(r'^homework/', views.homework, name='homework'),
    url(r'^import_student/', views.import_student, name='import_student'),
    url(r'^add_comment_score/$', views.add_comment_score, name='add_comment_score'),
    url(r'^delete_file/',views.delete_file,name='delete_file'),
    url(r'^edit_homework/',views.edit_homework,name='edit_homework'),
    url(r'^past_homeworks/',views.past_homeworks,name='past_homeworks'),


]
