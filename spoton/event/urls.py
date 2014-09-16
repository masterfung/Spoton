from __future__ import unicode_literals


from django.conf.urls import patterns, include, url
from django.db import IntegrityError
from rest_framework import viewsets, routers

from rest_framework.response import Response
from serializer import EventSerializer
from event.models import Event


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


router = routers.DefaultRouter()
router.register(r'event', EventViewSet)

urlpatterns = patterns('',
                       url(r'', include(router.urls)),
                       )