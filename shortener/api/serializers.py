from rest_framework import serializers
from core.models import AnonymousShortURL , UserLink , ClickEvent


class Anonnymousshorturlserializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousShortURL
        fields = '__all__'

class Clickeventserializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEvent
        fields = '__all__'


class UserlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLink
        fields = '__all__'

        