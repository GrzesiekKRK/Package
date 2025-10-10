from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy


from vehicles.forms import CreateVehicleForm, CreateVehicleDimensionForm


class VehicleCreateView(LoginRequiredMixin, CreateView):
    template_name = "vehicles/create_vehicle.html"
    success_url = reverse_lazy("dashboard")
    form_class = CreateVehicleForm
