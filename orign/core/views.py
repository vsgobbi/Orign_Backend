from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .serializers import ClientSerializer, HousesSerializer, VehiclesSerializer, \
    UpdatedClientSerializer,  RiskScoreSerializer, ClientUpdateSerialzier
from .models import Client, House, Vehicle, RiskScore


def option(request, client_id, car_id, house_id):

    vehicles = get_list_or_404(Vehicle, relevantdisease__pk=car_id)
    houses = get_list_or_404(House, relevantdisease__pk=car_id)
    client = get_object_or_404(Client, pk=client_id)

    context = {'client': client, 'houses': houses, 'vehicles': vehicles}
    #return render(request, "option.html", context)

#Working as JSON list GET on /houses/json
@api_view(['GET'])
def list_houses(request):

    if request.method == 'GET':
        houses = House.objects.all()
        serializer = HousesSerializer(houses, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    #Not working
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        houses = House.objects.all()
        serializer = HousesSerializer(House, data=data)
        #received_json_data = json.loads(request.body.decode("utf-8"))
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return Response(HousesSerializer.serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#url: /vehicles/json
@api_view(['GET'])
def list_vehicles(request):

    try:
        vehicles = Vehicle.objects.all()
    except Vehicle:
        return JsonResponse({'id': 'None'})
    if request.method == 'GET':
        serializer = VehiclesSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse(data={'id': 'None'}, status=400)


#url: /clients/json
@api_view(['GET', 'POST'])
def list_client(request):

    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = UpdatedClientSerializer(clients, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    else:
        return Response(UpdatedClientSerializer.serializer.errors, status=400)

#url: /post/id
#Working client CRUD
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def post_client(request, pk):

    serializer = ClientSerializer

    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return JsonResponse({'id': 'None'})

    if request.method == 'GET':
        instance = get_object_or_404(Client, pk=pk)
        instance.client = request.data.get('pk')
        serializer = ClientSerializer(instance)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        instance = get_object_or_404(Client, pk=pk)
        queryset = Client.objects.filter(id=pk)
        serializer = ClientSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        request = Client.objects.all()
        instance = get_object_or_404(request, pk=pk)
        serializer = ClientSerializer(instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        Client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        data = {'data': Client.objects.all()}
        return Response(data, status=400)
        #return Response(ClientSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientView(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            self.queryset = Client.objects.all().values('age', 'income', 'dependents', 'marital_status')
            return self.serializer_class
        if self.request.method == 'PUT':
            self.queryset = Client.objects.all().values('vehicles', 'houses', 'risk_questions')
            self.serializer_class = ClientUpdateSerialzier

        return self.serializer_class


class ClientUpdateView(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = UpdatedClientSerializer
    permission_classes = [permissions.AllowAny]


#url: /score
class RiskTest(generics.CreateAPIView):
#class RiskTest(generics.ListCreateAPIView):
    queryset = RiskScore.objects.all()
    serializer_class = RiskScoreSerializer

    #GETTING JSON list with CreateAPIView class
    def get(self, request, pk):
        instance = get_object_or_404(RiskScore, pk=pk)
        instance.client = request.data.get('pk')
        read_seriaizer = UpdatedClientSerializer(data=request.data)

        if request.method == 'GET':
            #clients = Client.objects.all()
            risk_scores = RiskScore.objects.all()
            serializer = RiskScoreSerializer(risk_scores, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({"id": "None"}, status=400)

    def get_queryset(self):
        instance = get_object_or_404(Client, pk=self.kwargs['pk'])
        instance.client = self.request.data
        self.queryset = UpdatedClientSerializer(data=self.request.data)
        return RiskScore.objects.filter(
        client = self.request.data,
        RiskScore = self.kwargs['pk'] #return queryset of model by current id
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            return RiskScoreSerializer
        return RiskScoreSerializer


class RiskScoreView(viewsets.ModelViewSet):

    queryset = RiskScore.objects.all()
    serializer_class = RiskScoreSerializer
    permission_classes = [permissions.AllowAny]


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
          if i['auto'] != 'null':
             i['client'] = None

        return Response(serializer.data)


class HousesView(viewsets.ModelViewSet):

    queryset = House.objects.all()
    queryClient = Client.objects.all()
    serializer_class = HousesSerializer
    permission_classes = [permissions.AllowAny]

    def get_json_houses(request):
        #houses = Client.objects.all().values('key', 'ownership_status')  # or simply .values() to get all fields
        houses = Client.objects.all()
        houses_list = list(houses)  # important: convert the QuerySet to a list object
        return JsonResponse(houses_list, safe=False)

    #Posting as JSON with viewsets.ModelViewSet
    def post_json(self, request, pk):
        instance = get_object_or_404(House, pk=pk)
        instance.client = request.data.get('pk')
        serializer = House()
        if request.method == 'POST':
            #return self.get_object()
            #return Response(serializer.data)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

   #GET JSON list with viewsets.ModelViewSet
    def get(self, request, pk):
        instance = get_object_or_404(House, pk=pk)
        instance.client = request.data.get('pk')
        serializer = House()
        if request.method == 'GET':
            #return self.get_object()
            #return Response(serializer.data)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class VehiclesView(viewsets.ModelViewSet):

    queryset = Vehicle.objects.all()
    serializer_class = VehiclesSerializer


#working PUT method to add Houses and Vehicles data to Client model
# "detail": "Method \"GET\" not allowed."
#url: clients/api/id
#class UpdateTest(generics.UpdateAPIView):
#Working PUT method as 'generics.UpdateAPIView'
class UpdateAPITest(generics.UpdateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        queryset = Client.objects.all().values('id', 'vehicles', 'houses', 'risk_questions')
        if request.method == 'GET':
            client = Client.objects.get(pk='id')
            instance = get_object_or_404(Client)
            instance.client = request.data.get('pk')
            serializer = ClientSerializer()
            #serializer = ClientUpdateSerializer(data=request.DATA)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = ClientSerializer(Client, data=request.data)
            if serializer.is_valid():
                instance = self.get_object()
                instance.save()
                serializer = self.get_serializer(instance)

                serializer.save(owner=instance.client)
                serializer.save()
                return JsonResponse(serializer.data)


#url: clients/view
class ClientViewSet(generics.ListCreateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]


