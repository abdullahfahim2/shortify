from rest_framework import generics
from .serializers import Anonnymousshorturlserializer , Clickeventserializer , UserlinkSerializer
from core.models import AnonymousShortURL


class Shorturlcreate(generics.ListCreateAPIView):
    queryset = AnonymousShortURL.objects.all()
    serializer_class = Anonnymousshorturlserializer



class ShortUrlDetail(generics.RetrieveUpdateAPIView):
    queryset = AnonymousShortURL.objects.all()
    serializer_class = Anonnymousshorturlserializer
    