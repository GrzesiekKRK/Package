from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView, LoginView
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from transport.forms import TransportForm, CargoDimensionForm
from transport.models import Transport, TransportStatus, CargoDimension

from notifications.views import OrderNotification
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
    def create_transport_status(request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        transport_form = TransportForm()
        cargo_dimension_form = CargoDimensionForm()

        if request.method == "POST":
            transport_form = TransportForm(request.POST)
            cargo_dimension_form = CargoDimensionForm(request.POST)

            if transport_form.is_valid() and cargo_dimension_form.is_valid():
                #DICT
                data = transport_form.cleaned_data
                data_for_calculation = {
                                        'collection_address': data['collection_address'],
                                        'delivery_address': data['delivery_address'],
                                        'notes': data['notes'],
                                        'price': data['price'],
                                        'total_distance': data['total_distance'],
                                        'total_duration': data['total_duration'],
                                        'transport_distance': data['transport_distance'],
                                        'transport_duration': data['transport_duration']
                                        }
                #FORMA dalej
                form_for_calculation = transport_form
                cargo_for_calculation = cargo_dimension_form
                ic(user)
                cargo_status = TransportStatus.objects.create(user=user)
                OrderNotification.client_notification(transport_status=cargo_status, user=user)
                OrderNotification.company_notification(transport_status=cargo_status, cargo_dimension=cargo_for_calculation, transport=form_for_calculation, user=user)
                return redirect("notification")

                # OrderNotification.client_notification(cargo_dimension=cargo_dimension, cargo=cargo, user=user,
                #                                       cargo_status=cargo_status)
                # OrderNotification.company_notification(cargo_dimension=cargo_dimension, cargo=cargo, user=user,
                #                                        cargo_status=cargo_status)
                # transport = transport_form.save(commit=False)
                # transport.cargo_status = cargo_status
                # transport.save()

                # cargo_dimension = cargo_dimension_form.save(commit=False)
                # cargo_dimension.transport = transport
                # cargo_dimension.save()

                # OrderNotification.client_notification(cargo_dimension=cargo_dimension, cargo=cargo, user=user, cargo_status=cargo_status)
                #
                # OrderNotification.company_notification(cargo_dimension=cargo_dimension, cargo=cargo, user=user, cargo_status=cargo_status)
                #
                # return render(request, "cargos/cargo_detail.html", {"cargo": cargo})

        context = {
            "cargo_form": transport_form,
            "cargo_dimension_form": cargo_dimension_form,
        }

        return render(request, "transport/create_transport.html", context)


class TransportStatusListView(LoginRequiredMixin, ListView):
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
        status = TransportStatus.objects.filter(user=self.request.user)
        context['transports'] = status

        return context


class TransportDetailView(LoginRequiredMixin, DetailView):
    model = Transport
    template_name = "transport/transport_detail.html"
