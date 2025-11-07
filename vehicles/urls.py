from django.urls import path

from vehicles.views import VehicleCreateView, VehicleListView, VehicleDetailView, VehicleUpdateView, VehicleDeleteView

urlpatterns = [
    path("create", VehicleCreateView.as_view(), name="create-vehicle"),
    path("list", VehicleListView.as_view(), name="vehicle-list"),
    path("<int:pk>/detail", VehicleDetailView.as_view(), name="vehicle-detail"),
    path("<int:pk>/update", VehicleUpdateView.as_view(), name="vehicle-update"),
    path("<int:pk>/delete", VehicleDeleteView.as_view(), name="vehicle-delete"),
]
