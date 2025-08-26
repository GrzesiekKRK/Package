from django.conf import settings
from django.db import models

from users.models import CustomUser


class Notification(models.Model):
    """Represents a notification of events like payment acceptance, wishlist product sale,
    and informing the vendor of sales.

    This model is used to store notifications for users, which can be read or unread.
    It helps keep users informed about various events or updates in the system.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    is_read = models.BooleanField(verbose_name="read", default=False)
    title = models.CharField(max_length=100)
    body = models.TextField()
    notes = models.CharField(max_length=900, blank=True, null=True, verbose_name="Additional information")# W templacie"About cargo and loading and unloading place"

    def __str__(self) -> str:
        return f"Notification of user {self.user} {self.body}"
