from django.conf.urls import url
from . import generic_views
from . import views

app_name = 'teacher'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_homework/', views.create_homework, name='create_homework'),
    url(r'^edit_course/', views.edit_course, name='edit_course'),
    url(r'^edit_homework/', views.edit_homework, name='edit_homework'),
    url(r'^course_info/', views.course_info, name='course_info'),
    url(r'^course_edit_form/(?P<pk>[0-9]+)$', generic_views.CourseUpdate.as_view()),
    url(r'^upload_file/', views.upload_file, name='upload_file'),
    url(r'^resources/', views.resources, name='resources'),
    url(r'^homework/', views.homework, name='homework'),
    url(r'^import_student/', views.import_student, name='import_student'),

]
