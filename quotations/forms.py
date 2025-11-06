from django import forms
from quotations.models import Quotation, VehiclePriceModificator


class CreateQuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
                    'transport',
                    'vehicle',
                    'kilometer_rate',
                    'toll_fee',
                    'fuel_consumption',
                    'driver_rate',
                    'maintenance_rate',
                    'minimal_profit',
                    'total_price']


class UpdateQuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
                    'vehicle',
                    'kilometer_rate',
                    'toll_fee',
                    'fuel_consumption',
                    'driver_rate',
                    'maintenance_rate',
                    'minimal_profit',
                    'total_price'
                ]


class CreateBasePriceModificatorForm(forms.ModelForm):
    class Meta:
        model = VehiclePriceModificator
        fields = [
            'vehicle_type',
            'value'
        ]

