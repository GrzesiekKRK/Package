from django.views.generic import CreateView, UpdateView, DetailView, ListView
from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from quotations.forms import CreateQuotationForm, UpdateQuotationForm, CreateBasePriceModificatorForm
from quotations.models import Quotation, BasePriceModificator

#TODO Dokończyć wycene
#TODO Dodać możliwość zrobienia kilku wycen
#TODO Wysyłanie tej najdroższej jako pierwszej najtańszej jako druga
class CreateQuotationView(LoginRequiredMixin, CreateView):
    model = Quotation
    template_name = "quotations/create_quotation.html"
    # success_url = reverse_lazy("user-sign-in")
    form_class = CreateQuotationForm


