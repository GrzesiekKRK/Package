from django.urls import path
from transport.views import CreateTransport, TransportDetailView, TransportStatusListView

urlpatterns = [
    path("cargos/create/", CreateTransport.create_transport_status, name="create-cargo"),
    path("cargo/<int:pk>/detail", TransportDetailView.as_view(), name="cargo-detail"),
    path("cargos/<int:pk>/statuses", TransportStatusListView.as_view(), name="cargo-list"),
]
