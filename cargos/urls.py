from django.urls import path
from cargos.views import CreateCargoTransport, CargoTransportDetailView, CargoTransportStatusListView

urlpatterns = [
    path("cargos/create/", CreateCargoTransport.create_cargo, name="create-cargo"),
    path("cargo/<int:pk>/detail", CargoTransportDetailView.as_view(), name="cargo-detail"),
    path("cargos/<int:pk>/statuses", CargoTransportStatusListView.as_view(), name="cargo-list"),
]
