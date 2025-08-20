from django import forms
from cargos.models import CargoTransport, CargoDimension


class CargoTransportForm(forms.ModelForm):
    class Meta:
        model = CargoTransport
        fields = [
            "total_distance",
            "total_duration",
            "transport_distance",
            "transport_duration",
            "price",
            "collection_address",
            "delivery_address",
        ]


class CargoDimensionForm(forms.ModelForm):
    class Meta:
        model = CargoDimension
        fields = [
            "length",
            "width",
            "height",
            "weight",
        ]
