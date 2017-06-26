from django.conf.urls import url

from . import views

app_name = 'teacher'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_homework/', views.create_homework, name='create_homework'),
    url(r'^edit_course/',views.edit_course,name='edit_course'),
    url(r'^edit_homework/',views.edit_homework,name='edit_homework'),

]
