from rest_framework import serializers
from django_filters import rest_framework
from .models import Sock

class SockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sock
        fields = ["id", "type", "hasHole"]