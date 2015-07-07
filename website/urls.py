from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^subject/(?P<subject>\w+)/$', views.subject, name='subject'),
    url(r'^subject/(?P<subject>\w+)/(?P<pk>\d+)/$', views.summary, name='summary'),
]
