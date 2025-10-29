from django.urls import path

from notifications.views import (
    NotificationDeleteView,
    NotificationDetailTemplateView,
    NotificationListTemplateView,
)

urlpatterns = [
    path("", NotificationListTemplateView.as_view(), name="notifications"),
    path(
        "<int:pk>/detail",
        NotificationDetailTemplateView.as_view(),
        name="notifications-detail",
    ),
    path(
        "<int:pk>/delete",
        NotificationDeleteView.as_view(),
        name="notifications-delete",
    ),
]
