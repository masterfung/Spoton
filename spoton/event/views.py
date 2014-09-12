from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from event.models import Event
from event.serializer import EventSerializer
from rest_framework import generics


class EventMixin(object):
    """
    This EventMixin is used for Bond's events.
    This code is recycled across different classes. It makes
    the most sense to abstract this out and use a mixin, as
    shown here.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventList(EventMixin, generics.ListCreateAPIView):
    """
    List all events in the DB, or allows the
    users to create new events.
    """
    permission_classes = (IsAuthenticated,)


class EventDetail(EventMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)