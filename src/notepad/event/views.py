from rest_framework import viewsets

from notepad.models import Event
from notepad.event.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer