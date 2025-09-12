from django import forms
from transport.models import Transport, CargoDimension


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = [
            "total_distance",
            "total_duration",
            "transport_distance",
            "transport_duration",
            "price",
            "collection_address",
            "delivery_address",
            "notes"
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
