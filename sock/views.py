# from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
# from rest_framework import viewsets
# from rest_framework.response import Response
# from .models import Sock
# from .serializers import SockSerializer

# class SockList(viewsets.ModelViewSet):
#     queryset = Sock.objects.all()
#     serializer_class = SockSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['type', 'hasHole']

import re
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sock
from .serializers import SockSerializer

class SockList(generics.ListCreateAPIView):
    '''
    Should list all socks with filtering abilities and create sock (less certain on the create).
    '''
    queryset = Sock.objects.all()
    serializer_class = SockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'hasHole']

# @api_view(['GET', 'POST'])
# def sock_list(request):
#     '''
#     List all socks, or create a new sock.
#     '''
#     if request.method == 'GET':
#         socks = Sock.objects.all()
#         serializer = SockSerializer(socks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         serializer = SockSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         error_msg = {'error':'Required field missing'}
#         return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','PUT','PATCH','DELETE'])
def sock_detail(request, pk):
    '''
    Retrieve, update, overwrite, or delete a specific sock.
    '''
    try:
        sock = Sock.objects.get(pk=pk)
    except Sock.DoesNotExist:
        # This handles any requests (GET, PUT, PATCH, DELETE) for a sock ID that doesn't exist
        error_msg={'error':'No such sock'}
        return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SockSerializer(sock)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SockSerializer(sock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"Required field missing"}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = SockSerializer(sock, data=request.data, partial=True) # partial is what allows this to be a patch method
        # I'm a little confused about the error handling in this one. I interpreted it as
        # if neither type or hasHole are included, return 400. Since I'm allowing for partial and assuming that this means
        # an empty field is still marked valid, and thus never hitting the second return, I'm catching
        # this neither conditon by checking the len of request.data to make sure it's not empty. 
        if serializer.is_valid() and len(request.data) > 0: 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"Required field missing"}, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'DELETE':
        sock.delete()
        return Response(status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def pair_list(request):
    '''
    List all matched pairs of socks.
    hmmmm, does the matching happen at the model level, or the serializer level?
    or else does it happens in views?
    '''
    if request.method == 'GET':
        pass
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        
    