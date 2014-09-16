# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.db import IntegrityError
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from rest_framework import viewsets, routers
from rest_framework.response import Response

from event.serializer import EventSerializer
from event.models import Event


# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#
#     def pre_save(self, obj):
#         obj.user = self.request.user
#
#     def create(self, request, *args, **kwargs):
#         try:
#             return super(EventViewSet, self).create(request, *args, **kwargs)
#         except IntegrityError:
#             return Response({
#                 'error': "You already submitted this URL!"
#             }, status=400)
#
# router = routers.DefaultRouter()
# router.register(r'event', EventViewSet)

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

    # url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^input/', include("event.urls")),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)