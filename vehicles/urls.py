from django.urls import path

from vehicles.views import VehicleCreateView

urlpatterns = [
    path("create/", VehicleCreateView.as_view(), name="create_vehicle"),
    path("list/", VehicleCreateView.as_view(), name="create_vehicle"),
]
