from django.urls import path
from cargos.views import CreateCargoTransport, CargoTransportDetailView, CargoTransportStatusListView

urlpatterns = [
    path("cargo/create/", CreateCargoTransport.create_cargo, name="create_cargo"),
    path("cargo/<int:pk>/detail", CargoTransportDetailView.as_view(), name="cargo-detail"),
    path("cargo/<int:pk>/cargos", CargoTransportStatusListView.as_view(), name="cargo-list"),
]
