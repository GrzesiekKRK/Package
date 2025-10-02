from django import forms
from quotations.models import Quotation


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['__all__']
