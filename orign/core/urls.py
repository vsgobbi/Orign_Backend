from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientView, 'Clients') #Handles the CRUD of Client model (OK)
router.register(r'updated_clients', views.ClientUpdateView, 'UpdatedClients')
router.register(r'houses', views.HousesView, 'Houses')
router.register(r'vehicles', views.VehiclesView, 'Vehicles')
router.register(r'riskscore', views.RiskScoreView, 'Scores')

urlpatterns = [

    path(r'', include(router.urls)),

    path(r'houses/json', views.list_houses), #test using Json parsers (OK) posting as JSON list!
    path(r'vehicles/json', views.list_vehicles), #test using Json parsers (OK) posting as JSON list!
    path(r'clients/json', views.list_client), #list all clients using Json parser

    path(r'score/<int:pk>', views.RiskTest.as_view()),
    path(r'clients/post/<int:pk>', views.post_client),

    path(r'clients/api/<int:pk>', views.UpdateAPITest.as_view()), #test ModelAPI

    path(r'clients/view/<int:pk>', views.ClientViewSet.as_view()),
]
