from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, DetailView, ListView, DeleteView
from users.permission import EmployeeRequiredMixin
from django.urls import reverse_lazy

from vehicles.forms import VehicleForm, VehicleDimensionForm
from vehicles.models import Vehicle


#TODO VehicleListView
class VehicleCreateView(EmployeeRequiredMixin, TemplateView):
    template_name = 'vehicles/create_vehicle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_form'] = VehicleForm(prefix='vehicle')
        context['vehicle_dimension_form'] = VehicleDimensionForm(prefix='dimension')
        return context

    def post(self, request, *args, **kwargs):
        vehicle_form = VehicleForm(request.POST, prefix='vehicle')
        is_tractor = request.POST.get('is_tractor') == 'on'

        if is_tractor:
            if vehicle_form.is_valid():
                vehicle = vehicle_form.save()
        else:
            vehicle_dimension_form = VehicleDimensionForm(request.POST, prefix='dimension')

            if vehicle_form.is_valid() and vehicle_dimension_form.is_valid():

                vehicle = vehicle_form.save()
                vehicle_dimension = vehicle_dimension_form.save(commit=False)
                vehicle_dimension.vehicle = vehicle
                vehicle_dimension.save()

        return redirect('dashboard')


class VehicleListView(EmployeeRequiredMixin, ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"


class VehicleDetailView(EmployeeRequiredMixin, DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"


class VehicleUpdateView(EmployeeRequiredMixin, UpdateView):
    model = Vehicle
    template_name = "vehicles/vehicle_update.html"
    form_class = VehicleForm
    success_url = reverse_lazy("vehicle-list")


class VehicleDeleteView(EmployeeRequiredMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicle-list")
