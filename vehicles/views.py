from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from icecream import ic

from vehicles.forms import CreateVehicleForm, VehicleDimensionForm


class VehicleCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'vehicles/create_vehicle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_form'] = CreateVehicleForm(prefix='vehicle')
        context['vehicle_dimension_form'] = VehicleDimensionForm(prefix='dimension')
        return context

    def post(self, request, *args, **kwargs):
        vehicle_form = CreateVehicleForm(request.POST, prefix='vehicle')
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




