from rest_framework import serializers
from .models import Event
from event.views import dispatch_url


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Events

    The first 'results' allows me to use the "get_results".
    SerializeMethodField is A field that gets its value by
    calling a method on the serializer it's attached to.

    The form will show only URL, Results and ID in the database.

    The URL is the user inputted link while the results will be the ten items returned.
    The Results will be contained in an array.
    ID is the representation of where the item is in the database.

    The method is defined through get_results, which returns the dispatch_url
    function defined in the event.views. dispatch_url is important for URL
    determination on whether it will be parsed as generic or not generics.

    """
    results = serializers.SerializerMethodField('get_results')

    class Meta:
        model = Event
        fields = 'url', 'results', 'id'

    def get_results(self, obj):
        # In case obj is of an Event
        return dispatch_url(obj.url)