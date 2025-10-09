from django.urls import path
from transports.views import CreateTransport, TransportDetailView, TransportStatusListView

urlpatterns = [
                path("transport/create/", CreateTransport.creation_manager, name="create-transport"),
                path("transport/<int:pk>/detail", TransportDetailView.as_view(), name="transport-detail"),
                path("transports/<int:pk>/statuses", TransportStatusListView.as_view(), name="transports-list"),
            ]
