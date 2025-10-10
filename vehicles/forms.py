from django import forms

from vehicles.models import Vehicle, VehicleDimension

#TODO Dokończyć widok tworzenia pojazdu
#TODO Dodać widok updatu pojazdu
#TODO Dodać w widoku update łączyć naczep z tractorem
class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "department",
            "type",
            "plates",
        )


class CreateVehicleDimensionForm(forms.Form):
    class Meta:
        model = VehicleDimension
        fields = (
            "vehicle",
            "length",
            "width",
            "height",
            "payload_capacity",
        )
