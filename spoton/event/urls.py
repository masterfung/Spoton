from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from rest_framework import viewsets
from event.models import Event
from spoton.event.serializer import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def pre_save(self, obj):
        obj.user = self.request.user

    def create(self, request, *args, **kwargs):
        try:
            return super(EventViewSet, self).create(request, *args, **kwargs)
        except IntegrityError:
            return Response({
                'error': "You already submitted this URL!"
            }, status=400)