from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView, LoginView
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from cargos.forms import CargoTransportForm, CargoDimensionForm
from cargos.models import CargoTransport, CargoTransportStatus, CargoDimension

from notifications.views import OrderNotification



#TODO link dla pracowniak z dodtkowe pytanie odośnie transportu
#TODO employee potwierdza wycen systemu i odsyła z automatu klientowi
#TODO po akceptacji ceny przez  kilenta  powstaje powiadomienie dla kierowcy i transportu
#TODO zmiana status na in progres i odbiorze ładunku stan trwa do rozładunku
#TODO widok potwierdzenia rozładunku przez klienta poprzez podanie kodu
#TODO bez logowania (tworzenie usera i ładunku naraz)
class CreateCargoTransport(LoginRequiredMixin, CreateView):
    model = CargoTransport
    template_name = "cargos/create_cargo.html"

    @staticmethod
    def create_cargo(request, *args, **kwargs):
        user = request.user
        cargo_form = CargoTransportForm()
        cargo_dimension_form = CargoDimensionForm()

        if request.method == "POST":
            cargo_form = CargoTransportForm(request.POST)
            cargo_dimension_form = CargoDimensionForm(request.POST)

            if cargo_form.is_valid() and cargo_dimension_form.is_valid():

                cargo_status = CargoTransportStatus.objects.create(user=user)

                cargo = cargo_form.save(commit=False)
                cargo.cargo_status = cargo_status
                cargo.save()

                cargo_dimension = cargo_dimension_form.save(commit=False)
                cargo_dimension.cargo = cargo
                cargo_dimension.save()

                OrderNotification.client_notification(cargo_dimension=cargo_dimension, cargo=cargo, user=user, cargo_status=cargo_status)

                OrderNotification.company_notification(cargo_dimension=cargo_dimension, cargo=cargo, user=user, cargo_status=cargo_status)

                return render(request, "cargos/cargo_detail.html", {"cargo": cargo})

        context = {
            "cargo_form": cargo_form,
            "cargo_dimension_form": cargo_dimension_form,
        }

        return render(request, "cargos/create_cargo.html", context)


class CargoTransportStatusListView(LoginRequiredMixin, ListView):
    model = CargoTransport
    template_name = "cargos/cargo_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Method that generates the context data to be passed to the template.

        **kwargs: Additional arguments passed to the method (e.g., URL variables).

        Returns:
            dict[str, Any]: A dictionary with data that will be used in the template.
        """
        context = super().get_context_data(**kwargs)
        status = CargoTransportStatus.objects.filter(user=self.request.user)
        context['cargos'] = status

        return context


class CargoTransportDetailView(LoginRequiredMixin, DetailView):
    model = CargoTransport
    template_name = "cargos/cargo_detail.html"
