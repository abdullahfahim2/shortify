from rest_framework import serializers
from core.models import AnonymousShortURL


class Anonnymousshorturlserializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousShortURL
        fields = '__all__'