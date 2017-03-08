from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^skill/list/$',
        login_required(views.SkillList.as_view()), name='skills'),
    url(r'^skill/(?P<pk>[0-9]+)/$',
        login_required(views.skill), name='skill'),
    url(r'^action/list/$',
        login_required(views.ActionList.as_view()), name='actions'),
    url(r'^action/(?P<pk>[0-9]+)/$',
        login_required(views.action), name='action'),
    url(r'^event/list/$',
        login_required(views.EventList.as_view()), name='events'),
    url(r'^event/(?P<pk>[0-9]+)/$',
        login_required(views.event), name='event'),
    url(r'^address/list/$',
        login_required(views.AddressList.as_view()), name='addresses'),
    url(r'^address/(?P<pk>[0-9]+)/$',
        login_required(views.address), name='address'),
    url(r'^person/list/$',
        login_required(views.people_list), name='people'),
    url(r'^person/(?P<pk>[0-9]+)/$',
        login_required(views.person), name='person'),
    url(r'^status/list/$',
        login_required(views.status_list), name='statuses'),
    url(r'^status/(?P<pk>[0-9]+)/$',
        login_required(views.status), name='status'),
    url(r'^period/list/$',
        login_required(views.PeriodList.as_view()), name='periods'),
    url(r'^search/$',
        login_required(views.search), name='search'),
]
