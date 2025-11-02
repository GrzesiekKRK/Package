from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from transports.forms import TransportForm, CargoDimensionForm
from transports.models import Transport, TransportStatus, CargoDimension

from notifications.views import CreateNotification
from icecream import ic

from users.models import CustomUser


#TODO link dla pracowniak z dodtkowe pytanie odośnie transportu
#TODO employee potwierdza wycen systemu i odsyła z automatu klientowi
#TODO po akceptacji ceny przez  kilenta  powstaje powiadomienie dla kierowcy i transportu
#TODO zmiana status na in progres i odbiorze ładunku stan trwa do rozładunku
#TODO widok potwierdzenia rozładunku przez klienta poprzez podanie kodu
#TODO bez logowania (tworzenie usera i ładunku naraz)
class CreateTransport(LoginRequiredMixin, CreateView):
    model = Transport
    template_name = "transport/create-transport.html"

    @staticmethod
    def transport_data(transport_form: TransportForm) -> Dict:
        """Create dict from form data """
        transport_data = transport_form.cleaned_data
        transport = {
                        'collection_address': transport_data['collection_address'],
                        'delivery_address': transport_data['delivery_address'],
                        'notes': transport_data['notes'],
                        'price': transport_data['price'],
                        'total_distance': transport_data['total_distance'],
                        'total_duration': transport_data['total_duration'],
                        'transport_distance': transport_data['transport_distance'],
                        'transport_duration': transport_data['transport_duration']
                           }
        return transport

    @staticmethod
    def create_transport(transport_form: TransportForm, transport_status: TransportStatus) -> Transport:
        """Create Transport object from dict"""
        transport = CreateTransport.transport_data(transport_form)

        instance = Transport(
                            transport_status=transport_status,
                            collection_address=transport['collection_address'],
                            delivery_address=transport['delivery_address'],
                            notes=transport['notes'],
                            price=transport['price'],
                            total_distance=transport['total_distance'],
                            total_duration=transport['total_duration'],
                            transport_distance=transport['transport_distance'],
                            transport_duration=transport['transport_duration']
                              )
        instance.save()
        return instance

    @staticmethod
    def cargo_data(cargo_dimension_form: CargoDimensionForm) -> Dict:
        """Create dict from form data """
        cargo_dimension_data = cargo_dimension_form.cleaned_data
        cargo_data = {
                        'weight': cargo_dimension_data['weight'],
                        'width': cargo_dimension_data['width'],
                        'height': cargo_dimension_data['height'],
                        'length': cargo_dimension_data['length']
                        }
        return cargo_data

    @staticmethod
    def create_cargo_dimension(cargo_dimension_form: CargoDimensionForm, transport: Transport) -> CargoDimension:
        """Create CargoDimension object from dict"""
        cargo_data = CreateTransport.cargo_data(cargo_dimension_form)
        cargo_dimension = CargoDimension(
                                        transport=transport,
                                        weight=cargo_data['weight'],
                                        width=cargo_data['width'],
                                        height=cargo_data['height'],
                                        length=cargo_data['length']
                                        )
        cargo_dimension.save()
        return cargo_dimension

    @staticmethod
    def create_transport_status(user: CustomUser) -> TransportStatus:
        """Create TransportStatus"""
        transport_status = TransportStatus.objects.create(user=user)
        return transport_status

    @staticmethod
    def notifications(transport_status: TransportStatus, cargo_dimension: CargoDimension, transport: Transport, user: CustomUser) -> None:
        """Create Notifications """
        CreateNotification.client_notification(transport_status=transport_status, user=user, transport=transport)
        CreateNotification.company_notification(
            transport_status=transport_status,
            cargo_dimension=cargo_dimension,
            transport=transport,
            user=user)

    @staticmethod
    def creation_manager(request, *args, **kwargs):
        """Manages creation of Transport Status/Transport/Cargo Dimension/Notifications"""
        user = CustomUser.objects.get(id=request.user.id)
        transport_form = TransportForm()
        cargo_dimension_form = CargoDimensionForm()

        if request.method == "POST":
            transport_form = TransportForm(request.POST)
            cargo_dimension_form = CargoDimensionForm(request.POST)
            if transport_form.is_valid() and cargo_dimension_form.is_valid():

                transport_status = CreateTransport.create_transport_status(user)
                transport = CreateTransport.create_transport(transport_form, transport_status)
                cargo_dimension = CreateTransport.create_cargo_dimension(cargo_dimension_form, transport)
                CreateTransport.notifications(transport_status, cargo_dimension, transport, user)

                return redirect("notifications")

        context = {
            "cargo_form": transport_form,
            "cargo_dimension_form": cargo_dimension_form,
        }

        return render(request, "transport/create_transport.html", context)

#TODO Spytać o query przez __user poniżej
class TransportListView(LoginRequiredMixin, ListView):
    """List all User Transports"""
    model = Transport
    template_name = "transport/transport_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Method that generates the context data to be passed to the template.

        **kwargs: Additional arguments passed to the method (e.g., URL variables).

        Returns:
            dict[str, Any]: A dictionary with data that will be used in the template.
        """
        context = super().get_context_data(**kwargs)
        # status = TransportStatus.objects.select_related('user').filter(user=self.request.user)
        # status_one = status[0]
        # transports = Transport.objects.select_related('transport_status', 'transport_status__user').filter(transport_status=status_one)
        transports = Transport.objects.select_related('transport_status', 'transport_status__user').filter(transport_status__user=self.request.user)

        context['transports'] = transports

        return context


class TransportDetailView(LoginRequiredMixin, DetailView):
    model = Transport
    template_name = "transport/transport_detail.html"


