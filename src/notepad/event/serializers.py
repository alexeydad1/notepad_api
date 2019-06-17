from rest_framework import serializers

from notepad.models import Event


class EventSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'
