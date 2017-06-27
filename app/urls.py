from django.conf.urls import url,include

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^sampleDB$', views.sampleDBView, name='sampleDB')
]
