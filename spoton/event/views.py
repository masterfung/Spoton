import urlparse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from event.models import Event
from event.serializer import EventSerializer
from rest_framework import generics
from event.forms import EventForm
import re
from requests import get
from bs4 import BeautifulSoup


# class EventMixin(object):
#     """
#     This EventMixin is used for Bond's events.
#     This code is recycled across different classes. It makes
#     the most sense to abstract this out and use a mixin, as
#     shown here.
#     """
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#
#
# class EventList(EventMixin, generics.ListCreateAPIView):
#     """
#     List all events in the DB, or allows the
#     users to create new events.
#     """
#     permission_classes = (IsAuthenticated,)
#
#
# class EventDetail(EventMixin, generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAdminUser,)


# def event_search_input(request):
#     event = Event.objects.filter(user=request.user)
#
#     if 'event' in request.POST:
#         event_form = EventForm(request.POST, prefix='event')
#         if event_form.is_valid():
#             event = event_form.save(commit=False)
#             event.user = request.user
#             event.save()
#             return redirect('/profile')
#     else:
#         event_form = EventForm(prefix='event')
#     data = {'user': request.user, 'event': event, 'event_form': event_form}
#     return render(request, 'rest_overwrite.html', data)


def incrementor(match):
    before, number, after = match.groups()
    number = int(number) + 1
    return '%s%d%s' % (before, number, after)


def url_regex(url):
    result = re.sub('^(http[s]?://.*[^0-9])([0-9]+)([^0-9]?)$', incrementor, url)
    if result != url:
        return result
    return re.sub(r'(.*/)[^/]*', r'\1', result)


def consecutive_incrementor(amount, url):
    results = []
    for _ in xrange(amount):
        url = url_regex(url)
        results.append(url)
    return results


first = 'http://calendar.boston.com/lowell_ma/events/show/274127485-mrt-presents-shakespeares-will'
second = 'http://www.sfmoma.org/exhib_events/exhibitions/513'
third = 'http://www.workshopsf.org/?page_id=140&id=1328'
fourth = 'http://events.stanford.edu/events/353/35309/'
eventbrite_link = 'http://www.eventbrite.com/e/sausalito-art-festival-2014-tickets-11831764125?aff=ehometext&rank=0'


def handle_eventbrite_url(url):
    working_var = url
    result = re.search('^(http[s]?://.*[^0-9].com)', working_var)
    final = result.group()
    r = get(final)
    soup = BeautifulSoup(r.content)

    eventbrite_match = re.compile('(http://www.eventbrite.com/e/)')
    links = soup.find_all('a')
    # for link in links:
    #     print link.get('href')

    # print links
    output = []
    for link in links:
        try:
            href = link['href']
            if re.search(eventbrite_match, href):
                output.append(href)

            if len(output) == 10:
                break

        except KeyError:
            pass

    return output


def handle_generic_url(url):
    chomp = url_regex(url)
    print chomp

    first_expected = 'http://calendar.boston.com/lowell_ma/events/show/'

    match = re.compile('(/boston_ma/events/show/)')

    if chomp == first_expected:
        output = set()
        r = get(first_expected)

        if r.status_code != 200:
            print 'request has errors!'
            return

        soup = BeautifulSoup(r.content)

        for link in soup.find_all('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    output.add(urlparse.urljoin(url, href))

                if len(output) == 10:
                    break

            except KeyError:
                pass

        return list(output)
    else:
        return consecutive_incrementor(10, chomp)


url_handlers = {
    'www.eventbrite.com': handle_eventbrite_url
}


def dispatch_url(url):
    parsed = urlparse.urlparse(url)
    handler = url_handlers.get(parsed.hostname, handle_generic_url)
    return handler(url)


# second = 'http://www.sfmoma.org/exhib_events/exhibitions/513'
# second_expected = 'http://www.sfmoma.org/exhib_events/exhibitions/514'
# assert url_regex(second) == second_expected
#
# third = 'http://www.workshopsf.org/?page_id=140&id=1328'
# third_expected = 'http://www.workshopsf.org/?page_id=140&id=1329'
# assert url_regex(third) == third_expected
#
# fourth = 'http://events.stanford.edu/events/353/35309/'
# fourth_expected = 'http://events.stanford.edu/events/353/35310/'
# assert url_regex(fourth) == fourth_expected
#
# print url_regex(first)
#
# print consecutive_incrementor(10, fourth)

# assert consecutive_incrementor(3, fourth) == ['http://events.stanford.edu/events/353/35310/',
#                                               'http://events.stanford.edu/events/353/35311/',
#                                               'http://events.stanford.edu/events/353/35312/']