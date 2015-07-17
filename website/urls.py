from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^subject/(?P<subject>\w+)/$', views.subject, name='subject'),
        url(r'^subject/(?P<subject>\w+)/(?P<division_name>\w+)/$',
        views.division, name='division'),
    url(r'^subject/(?P<subject>\w+)/(?P<division_name>\w+)/(?P<pk>\d+)/$',
        views.summary, name='summary'),
    url(r'^subject/(?P<subject>\w+)/(?P<pk>\d+)/edit$',
        views.edit_summary, name='edit_summary'),
    url(r'^rate_summary/$', views.rate_summary, name='rate_summary'),
    url(r'^search/$', views.search, name='search'),
    url(r'^upload/$', views.upload, name='upload'),
]
