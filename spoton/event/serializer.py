from rest_framework import serializers
from .models import Event
from event.views import dispatch_url


class EventSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField('get_results')

    class Meta:
        model = Event
        fields = 'url', 'results', 'id'

    def get_results(self, obj):
        # In thie case  obj is of an Event
        return dispatch_url(obj.url)