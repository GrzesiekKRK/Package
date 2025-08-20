from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView, LoginView
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView, DetailView

from cargos.forms import CargoTransportForm, CargoDimensionForm
from cargos.models import CargoTransport, CargoTransportStatus, CargoDimension
from users.forms import RegisterUserForm


#Funkcja tworzenia bez logowania
class CreateCargoTransport(CreateView):
    model = CargoTransport
    template_name = "cargos/create_cargo.html"

    @staticmethod
    def create_cargo(request, *args, **kwargs):
        if not request.user.is_authenticated:
            user = RegisterUserForm()
        else:
            user = request.user
        cargo_form = CargoTransportForm()
        cargo_dimension_form = CargoDimensionForm()
        if cargo_form.is_valid() and cargo_dimension_form.is_valid():
            cargo_status = CargoTransportStatus(user)
            cargo_status.save()
            cargo = CargoTransportForm(cargo_status.id, cargo_form)
            cargo.save()
            cargo_dimension = CargoDimension(cargo, cargo_dimension_form)
            cargo_dimension.save()

        context = {
                "cargo_form": cargo_form,
                "cargo_dimension_form": cargo_dimension_form,
                "user_form": user,
        }

        return render(request, "cargos/create_cargo.html", context)
