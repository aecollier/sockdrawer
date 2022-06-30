from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.
from .models import Sock
from .serializers import SockSerializer

class SockList(viewsets.ModelViewSet):
    serializer_class = SockSerializer
    queryset = Sock.objects.all()
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'hasHole']
    
    # def list(self, request):
    #     serializer = SockSerializer(queryset)
    #     return Response(serializer.data)
    