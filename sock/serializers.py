'''
I created these serializers.
'''
from rest_framework import serializers
from django_filters import rest_framework
from .models import Sock, Pair

class SockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sock
        fields = ["id", "type", "hasHole"]

class PairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pair
        fields = ["type","socks"]