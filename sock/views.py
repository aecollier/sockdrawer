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
    # how to implement that explicitly with the generic api view. 


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
#         # was able to explicitly pass the 405 here, which I liked, but needed to use generic view to get filtering functionality!
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','PUT','PATCH','DELETE'])
def sock_detail(request, id):
    '''
    Retrieve, update, overwrite, or delete a sock.
    '''
    try:
        sock = Sock.objects.get(id=id)
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
    '''
    if request.method == 'GET':
        # filter for socks without holes
        socks = Sock.objects.filter(hasHole=False)
        # Get a dictionary mapping id to color (this is my way to work with the queryset but not sure it's the smartest as it requires conversion back later)
        types = {t.id:t.type for t in Sock.objects.all()} 
        #print(types) # {1: 'yellow', 2: 'black', 3: 'green', 4: 'blue', 5: 'blue'}
        # get a counter of how many there are of each type
        counts = Counter(list(types.values()))
        #print(counts) # Counter({'blue': 2, 'yellow': 1, 'black': 1, 'green': 1})
        pairs_obj = [] # to hold list of JSON objects
        dic_one_type = {} # To represent a JSON object with type and socks
        id_list = [] # list of id's in sock pairs

        for k,v in counts.items():
            if v>=2:
                k_socks = Sock.objects.filter(type=k) # query for sock of k type
                print(k_socks)
                unpaired_socks = v # get number of socks we start with
                while unpaired_socks > 1:
                    id_list.append(k_socks[0].id)
                    id_list.append(k_socks[1].id)
                    k_socks=k_socks[2:] #chop off the two we just looked at, maybe?
                    dic_one_type["type"] = k
                    dic_one_type["socks"] = id_list
                    if dic_one_type not in pairs_obj:
                        pairs_obj.append(dic_one_type)
                    unpaired_socks -= 2 # decrement unpaired sock count by 2
                    id_list = [] # reset
                    dic_one_type = {} # reset
            
        print('Pairs dict ',pairs_obj)
        if len(pairs_obj)==0:
            return Response({"error":"No matching pairs"}, status=status.HTTP_404_NOT_FOUND)

            # if v>=2: # if there's a count of more than one
            #     single_type = Sock.objects.filter(type=k) # this gets a color where there's more than one sock
            #     print(k) # blue
            #     match_ids = [s.id for s in single_type] # this is the list of ids we want, but all of them. [4,5]
            #     pairs_dic[k] = match_ids
                # do something next that chunks that into pairs 
                # then builds the ids and pairs into a json object to pass to Pairs, I think.
                # I think I can build a json object and then "deserialize" it with the Pair serializer.
                # https://www.adamsmith.haus/python/answers/how-to-create-a-json-object-in-python
                # not sure this one is useful but https://stackoverflow.com/questions/57699169/django-drf-how-to-deserialize-an-instance-that-requires-a-foreign-key
                # https://www.django-rest-framework.org/api-guide/serializers/#deserializing-objects
                # Do I need the pairs model for this to work? I'm thinking maybe yes, since Socks isn't in the right format/has different fields!
                # Oooh, I think this approach also validates the JSONField I use. Need to research that a little more.
        json_dump = json.dumps(pairs_obj)
        json_object = json.loads(json_dump)
        #pairs = JSONParser().parse(json_object)
        serializer = PairSerializer(json_object, many=True)  
        print(serializer)
        #print(serializer.data)  
        #serializer2 = SockSerializer(socks, many=True)
        #print(serializer2)
        #print(serializer2.data)
        #print(SockSerializer)
        return Response(serializer.data, status=status.HTTP_200_OK)



        # visited = set()
        # dup = set([x for x in list(types.values()) if x in visited or (visited.add(x) or False)])
        # print(types)
        # print(dup)
        # for t in dup:
        #     one_type = Sock.objects.filter(type=t)
        #     if len(one_type)%2 == 0:

        if len(socks) > 1:
            for i in range(1, len(socks)+1):
                pass
                # is there an implementation that doesn't require looping through all of the socks?
                #current = Sock.objects.get(id=i)
                #print(Sock.objects.get(id=i).type)

            serializer = SockSerializer(socks, many=True)    
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# class PairsList(generics.ListAPIView):
#     '''
#     List any existing pairs of socks.
#     '''
#     queryset = Sock.objects.all()
#     serializer_class = SockSerializer
#     if len(queryset) > 1:
#         first = Sock.objects.get(id=1)
#         print(first)
#             # sock__type


        
    