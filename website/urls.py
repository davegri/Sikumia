from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
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
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt")),
]
