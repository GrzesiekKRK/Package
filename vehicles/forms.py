from django import forms

from vehicles.models import Vehicle, VehicleDimension


class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "department",
            "type",
            "plates",
        )


class VehicleDimensionForm(forms.ModelForm):
    class Meta:
        model = VehicleDimension
        fields = (
            "length",
            "width",
            "height",
            "payload_capacity",
        )
