from rest_framework import viewsets

from notepad.models import Note
from notepad.note.serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer