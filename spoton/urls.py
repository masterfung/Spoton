# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from rest_framework import viewsets, routers
from event.models import Event
from event.serializer import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

router = routers.DefaultRouter()
router.register(r'event', EventViewSet)

urlpatterns = patterns('',
    url(r'^$',  # noqa
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),

    # Uncomment the next line to enable the admin:
    url(r'^spotonadmin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^api/events/$', EventList.as_view(), name='event_list'),
    # url(r'^api/events/(?P<pk>[0-9]+)/$', EventDetail.as_view(), name='event_detail'),

    # url(r'^events/$', 'event.views.event_search_input', name='event_search_input'),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)