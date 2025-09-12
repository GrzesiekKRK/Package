from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView, LoginView
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from transport.forms import TransportForm, CargoDimensionForm
from transport.models import Transport, TransportStatus, CargoDimension

from notifications.views import OrderNotification
from icecream import ic


#TODO link dla pracowniak z dodtkowe pytanie odośnie transportu
#TODO employee potwierdza wycen systemu i odsyła z automatu klientowi
#TODO po akceptacji ceny przez  kilenta  powstaje powiadomienie dla kierowcy i transportu
#TODO zmiana status na in progres i odbiorze ładunku stan trwa do rozładunku
#TODO widok potwierdzenia rozładunku przez klienta poprzez podanie kodu
#TODO bez logowania (tworzenie usera i ładunku naraz)
class CreateTransport(LoginRequiredMixin, CreateView):
    model = Transport
    template_name = "cargos/create_cargo.html"

    @staticmethod
    def create_transport_status(request, *args, **kwargs):
        user = request.user
        transport_form = TransportForm()
        cargo_dimension_form = CargoDimensionForm()

        if request.method == "POST":
            transport_form = TransportForm(request.POST)
            cargo_dimension_form = CargoDimensionForm(request.POST)

            if transport_form.is_valid() and cargo_dimension_form.is_valid():
                #DICT
                ic(transport_form.cleaned_data)
                ic(transport_form)
                # cargo_status = TransportStatus.objects.create(user=user)
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

        return render(request, "cargos/create_cargo.html", context)


class TransportStatusListView(LoginRequiredMixin, ListView):
    model = Transport
    template_name = "cargos/cargo_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Method that generates the context data to be passed to the template.

        **kwargs: Additional arguments passed to the method (e.g., URL variables).

        Returns:
            dict[str, Any]: A dictionary with data that will be used in the template.
        """
        context = super().get_context_data(**kwargs)
        status = TransportStatus.objects.filter(user=self.request.user)
        context['cargos'] = status

        return context


class TransportDetailView(LoginRequiredMixin, DetailView):
    model = Transport
    template_name = "cargos/cargo_detail.html"
