from django.conf.urls import url

from . import views

app_name = 'system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^uploadStudents$', views.upload_students, name='uploadStudent'),
    url(r'^uploadTeachers$', views.upload_teachers, name='uploadTeachers'),
    url(r'^createTerm$', views.create_term, name='createTerm'),
    url(r'^createCourse$', views.create_course, name='createCourse'),
    url(r'^showTerm$', views.show_term, name='showTerm'),
]