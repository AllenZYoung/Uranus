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
    url(r'^showCourse$', views.show_course, name='showCourse'),
    url(r'^editTerm$', views.edit_term, name='editTerm'),
    url(r'editCourse$', views.edit_course, name='editCourse'),
    url(r'^loadStudents$', views.load_student, name='loadCourse'),
]