from django import forms
from quotations.models import Quotation


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['__all__']


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
