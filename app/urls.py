from django.conf.urls import url,include

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
