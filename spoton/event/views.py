from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from event.models import Event
from event.serializer import EventSerializer
from rest_framework import generics
from event.forms import EventForm
import re


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


def EventSearch(request):
    event = Event.objects.filter(user=request.user)

    if request.POST:
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('/profile')
    else:
        event_form = EventForm()
    data = {'user': request.user, 'event': event, 'event_form': event_form}
    return render(request, 'users/user_detail.html', data)


def callable(match):
    before, number, after = match.groups()
    number = int(number) + 1
    return '%s%d%s' % (before, number, after)


def go(url):
    result = re.sub('^(http[s]?://.*[^0-9])([0-9]+)([^0-9]?)$', callable, url)
    if result != url:
        return result
    return re.sub(r'(.*/)[^/]*', r'\1', result)


def consecutive(amount, url):
    results = []
    for _ in xrange(amount):
        url = go(url)
        results.append(url)
    return results


first = 'http://calendar.boston.com/lowell_ma/events/show/274127485-mrt-presents-shakespeares-will'
first_expected = 'http://calendar.boston.com/lowell_ma/events/'

second = 'http://www.sfmoma.org/exhib_events/exhibitions/513'
second_expected = 'http://www.sfmoma.org/exhib_events/exhibitions/514'
assert go(second) == second_expected

third = 'http://www.workshopsf.org/?page_id=140&id=1328'
third_expected = 'http://www.workshopsf.org/?page_id=140&id=1329'
assert go(third) == third_expected

fourth = 'http://events.stanford.edu/events/353/35309/'
fourth_expected = 'http://events.stanford.edu/events/353/35310/'
assert go(fourth) == fourth_expected

print go(first)

print consecutive(3, fourth)

assert consecutive(3, fourth) == ['http://events.stanford.edu/events/353/35310/',
                                  'http://events.stanford.edu/events/353/35311/',
                                  'http://events.stanford.edu/events/353/35312/']