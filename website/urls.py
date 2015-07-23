from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/(?P<user_pk>\d+)$', views.profile, name='profile'),
        url(r'^subject/(?P<subject>\w+)/(?P<category>[\w-]+)/(?P<summary_id>\d+)/$',
        views.summary, name='summary'),
    url(r'^subject/(?P<subject>\w+)/(?P<category>[\w-]+)/(?P<summary_id>\d+)/edit/$',
        views.edit_summary, name='edit_summary'),
    url(r'^subject/(?P<subject>\w+)/$', views.subject, name='subject'),
    url(r'^subject/(?P<subject>\w+)/(?P<category>[\w-]+)/$', views.category, name='category'),
    url(r'^subject/(?P<subject>\w+)/(?P<category>[\w-]+)/(?P<subcategory>[\w-]+)/$', views.subcategory, name='subcategory'),
    url(r'^rate_summary/$', views.rate_summary, name='rate_summary'),
    url(r'^search/$', views.search, name='search'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^get_categories/(?P<subject_id>\d+)/$', views.get_categories, name='get_categories'),
    url(r'^get_subcategories/(?P<category_id>\d+)/$', views.get_subcategories, name='get_subcategories'),
]
