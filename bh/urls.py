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
    url(r'^action/types/$',
        login_required(views.ActionCategoryList.as_view()), name='action_types'),
    url(r'^action/type/(?P<pk>[0-9]+)/$',
        login_required(views.action_type), name='action_type'),
    url(r'^action/(?P<pk>[0-9]+)/$',
        login_required(views.action), name='action'),
    url(r'^event/types/$',
        login_required(views.EventCategoryList.as_view()), name='event_types'),
    url(r'^event/type/(?P<pk>[0-9]+)/$',
        login_required(views.event_type), name='event_type'),
    url(r'^event/(?P<pk>[0-9]+)/$',
        login_required(views.event), name='event'),
    url(r'^address/list/$',
        login_required(views.AddressList.as_view()), name='addresses'),
    url(r'^address/(?P<pk>[0-9]+)/$',
        login_required(views.address), name='address'),
    url(r'^person/list/$',
        login_required(views.people_list), name='people'),
    url(r'^person/birthdays/list/$',
        login_required(views.people_birthdays_list), name='birthdays'),
    url(r'^person/(?P<pk>[0-9]+)/$',
        login_required(views.person), name='person'),
    url(r'^search/$',
        login_required(views.search), name='search'),
]
