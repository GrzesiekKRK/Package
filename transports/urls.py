from django.urls import path
from transports.views import CreateTransport, TransportDetailView, TransportStatusListView

urlpatterns = [
                path("cargos/create/", CreateTransport.creation_manager, name="create-transport"),
                path("cargo/<int:pk>/detail", TransportDetailView.as_view(), name="cargo-detail"),
                path("cargos/<int:pk>/statuses", TransportStatusListView.as_view(), name="cargo-list"),
            ]
