from django.conf.urls import url

from . import views

app_name = 'system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^uploadStudents$', views.upload_students, name='uploadStudent'),
    url(r'uploadTeachers$',views.upload_teachers, name='uploadTeachers'),
]