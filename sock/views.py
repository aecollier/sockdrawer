from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sock
from .serializers import SockSerializer, PairSerializer

from collections import Counter
import json

class SockList(generics.ListCreateAPIView):
    '''
    List all socks, with optional url filtering, or create a new sock. 
    '''
    # Using GenericAPIView to simplify basic GET/POST functionality, with filtering.
    queryset = Sock.objects.all() 
    serializer_class = SockSerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'hasHole']

    # overwrote create so I could return specific error message.
    def create(self, request):
        serializer = SockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        error_msg = {'error':'Required field missing'}
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    # Making some assumptions that attempting other methods returns 405 - not sure 
    # how to implement that explicitly within the generic api class view. Had it explicitly implemented
    # with function based view first, as below.


@api_view(['GET','PUT','PATCH','DELETE'])
def sock_detail(request, id):
    '''
    Retrieve, update, overwrite, or delete a sock.
    '''
    # Decided to keep the more verbose function api views here, as I like that I can be exact with error messages and codes.
    try:
        sock = Sock.objects.get(id=id)
    except Sock.DoesNotExist:
        # This handles any requests (GET, PUT, PATCH, DELETE) for a sock ID that doesn't exist
        error_msg={'error':'No such sock'}
        return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SockSerializer(sock) # convert queryset to Python datatype
        return Response(serializer.data) # return response object of query data

    elif request.method == 'PUT':
        serializer = SockSerializer(sock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"Required field missing"}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = SockSerializer(sock, data=request.data, partial=True) # partial is what allows this to be a patch method
        # I'm a little unclear on the error handling in this one. I interpreted it as
        # if neither type or hasHole are included (an empty request body), return 400. Including partial=True seems to allow
        # an empty request body to still be marked valid, so it never hits the second return. I'm catching neither specified
        # conditon by checking the len of request.data to make sure it's not empty. 
        if serializer.is_valid() and len(request.data) > 0: 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"Required field missing"}, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'DELETE':
        sock.delete()
        return Response(status=status.HTTP_200_OK)

    else:
        # If another not implemented request is sent, return 405.
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def pair_list(request):
    '''
    List all matched pairs of socks.
    '''
    if request.method == 'GET':
        # filter for socks without holes
        socks = Sock.objects.filter(hasHole=False)
        
        # create a dictionary mapping id to color to make sock data more Pythonic to work with (what my brain needs, for now)
        types = {t.id:t.type for t in socks} 

        # count how many socks of each type exist
        counts = Counter(list(types.values()))

        pairs_obj = [] # a list of pair objects
        dic_one_type = {} # a dictionary representing a pair instance with "type" and "socks" keys
        id_list = [] # a list of id's in a sock pair

        for k,v in counts.items():
            if v>=2:
                k_socks = Sock.objects.filter(type=k) # query for socks of k type
                unpaired_socks = v # get total number of socks to start with
                while unpaired_socks > 1:
                    id_list.append(k_socks[0].id) # add two socks to a pair
                    id_list.append(k_socks[1].id)
                    k_socks=k_socks[2:] # chop off the two we just added, to ensure they don't get added more than once
                    dic_one_type["type"] = k
                    dic_one_type["socks"] = id_list
                    if dic_one_type not in pairs_obj: # make sure no duplicate entries
                        pairs_obj.append(dic_one_type)
                    unpaired_socks -= 2 # decrement unpaired sock count by 2
                    id_list = [] # reset
                    dic_one_type = {} # reset
            
        if len(pairs_obj)==0:
            # if there are no matching pairs return 404
            return Response({"error":"No matching pairs"}, status=status.HTTP_404_NOT_FOUND)

        # turn the dictionary into a JSON object
        json_dump = json.dumps(pairs_obj)
        pairs = json.loads(json_dump)
        # here, using the deserializing function of DRF serializers to convert my JSON object back to a complex type
        serializer = PairSerializer(pairs, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



        
    