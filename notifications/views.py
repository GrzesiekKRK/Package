from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView, TemplateView

from transport.models import TransportStatus, Transport, CargoDimension
from notifications.models import Notification
from users.models import CustomUser, Employee, Department


class NotificationListTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "notifications/notification.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Retrieves notifications for the logged-in user and passes them to the template.
        The notifications are ordered by their 'is_read' status, so unread notifications
        appear first.

        Args:
            **kwargs: Additional keyword arguments passed to the method.
                      This includes any URL variables or context data.

        Returns:
            dict[str, Any]: A dictionary of context data for rendering the template.
                             Contains the list of notifications under the key 'notifications'.
        """
        notification = Notification.objects.filter(user=self.request.user.id).order_by(
            "is_read"
        )
        paginator = Paginator(notification, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        page_obj = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context["notifications"] = page_obj
        return context


class NotificationDetailTemplateView(LoginRequiredMixin, TemplateView):
    model = Notification
    template_name = "notifications/notification-detail.html"

    def get_object(self, queryset=None) -> Notification:
        """
        Retrieves the notification based on its primary key (pk).
        Only allows access if the notification belongs to the logged-in user.

        Args:
            queryset (QuerySet, optional): A queryset used to fetch the object (not used here).

        Returns:
            Notification: The notification object associated with the provided pk.

        Raises:
            Http404: If the notification is not found or the logged-in user does not have permission.
        """
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"])

        if notification.user != self.request.user:
            raise Http404(
                "Notification not found or you don't have permission to view it."
            )
        return notification

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Retrieves the context for the notification details page and marks the notification as read.

        Args:
            **kwargs: Additional keyword arguments passed to the method.
                      This includes any URL variables or context data.

        Returns:
            dict[str, Any]: A dictionary of context data, including the notification's title, body,
                             and read status.
        """
        context = super().get_context_data(**kwargs)
        notification = self.get_object()

        read = notification.is_read
        if not read:
            read = NotificationDetailTemplateView.read(notification)
        context["notification"] = notification
        context["title"] = notification.title
        context["body"] = notification.body

        return context

    @staticmethod
    def read(notification: Notification) -> Notification:
        """
        Marks the given notification as read and saves it.

        Args:
            notification (Notification): The notification instance to mark as read.

        Returns:
            Notification: The updated notification instance with is_read set to True.
        """
        notification.is_read = True
        notification.save()
        return notification


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    """Handles the deletion of a notification."""

    model = Notification
    template_name = "notifications/notification_confirm_delete.html"
    success_url = "/products/"

    def get_object(self, queryset=None) -> Notification:
        """
        Retrieves the notification to be deleted.
        Ensures the notification belongs to the logged-in user before allowing deletion.

        Args:
            queryset (QuerySet, optional): A queryset used to fetch the object (not used here).

        Returns:
            Notification: The notification instance that will be deleted.

        Raises:
            Http404: If the notification does not exist or the logged-in user does not have permission.
        """
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"])

        if notification.user != self.request.user:
            raise Http404(
                "Notification not found or you don't have permission to view it."
            )
        return notification

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Passes the notification to the context so the user can confirm its deletion.

        Args:
            **kwargs: Additional keyword arguments passed to the method.
                      This includes any URL variables or context data.

        Returns:
            dict[str, Any]: A dictionary of context data, including the notification to be deleted.
        """
        context = super().get_context_data(**kwargs)
        context["notification"] = self.get_object()
        return context


class OrderNotification:
    """Handles creating notifications related to orders, such as payment acceptance and vendor updates."""

    @staticmethod
    def client_notification(cargo_status: TransportStatus, cargo: Transport, cargo_dimension: CargoDimension, user: CustomUser ) -> Notification:
        """
        Creates and sends a notification to the buyer when their payment is accepted.

        Args:
            order (Order): The order instance for which the notification is created.

        Returns:
            Notification: The created notification instance sent to the buyer.
        """
        title = f"{cargo_status.id} awaiting verification"
        body = (f"'Hi your transport demand will be check and evaluation."
                f" Once done will send notification with price tag and possible dates if your date we are occcupices."
                f" If you accept price confimet by paying with link in notification:"
                f" <a href=\"http://127.0.0.1:8000/order/detail/{cargo_status.id}\">"
                f"<i class='fas fa-envelope me-2 text-secondary'>"
                f"</i>Open notification</a>'")
        user_notification = Notification(user=user, title=title, body=body)
        user_notification.save()
        return user_notification

    @staticmethod
    def company_notification(cargo_status: TransportStatus, cargo: Transport, cargo_dimension: CargoDimension, user: CustomUser) -> Notification:
        """
        Creates and sends a notification to the vendor when their products are sold.

        Args:
            order (Order): The order instance for which the notification is created.

        Returns:
            Notification: The created notification instance sent to the vendor.
        """

        department, created = Department.objects.get_or_create(id=1, address="Kraków Ćwiartki 3/4")
        office_employee, created = Employee.objects.get_or_create(
            department=department,
            username="Tomek",
            first_name="Tomek",
            last_name="Benaruczak",
            email="Package@office.pl",
            postal_code="34-587",
            billing_address="Zator",
            payroll_account="12345678901234567890123456",

        )
        if created:
            office_employee.set_password("pass")
            office_employee.save()
        office_title = f"{cargo.id} awaiting verification"
        office_body = (
            f"'Hi Mr/Mrs {user.first_name} {user.last_name} contact {user.email}/ {user.phone_number} made a transport demand that need evaluation."
            f" Here are it data."
            f" {cargo}"
            f" {cargo_dimension}"
        )

        company_notification = Notification(user=office_employee, title=office_title, body=office_body)
        company_notification.save()
        return company_notification
