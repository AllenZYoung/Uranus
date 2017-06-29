from django.conf.urls import url, include
from django.conf.urls import handler404

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^change_info/', views.change_info, name='change_info'),
]
