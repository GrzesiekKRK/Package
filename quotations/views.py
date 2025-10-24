from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView
from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from quotations.forms import CreateQuotationForm, UpdateQuotationForm, CreateBasePriceModificatorForm
from quotations.models import Quotation, BasePriceModificator
from users.permission import EmployeeRequiredMixin
from notifications.models import Notification
from transports.models import Transport
from icecream import ic

#TODO Dokończyć wycene
#TODO Dodać możliwość zrobienia kilku wycen
#TODO Wysyłanie tej najdroższej jako pierwszej najtańszej jako druga
class CreateQuotationView(EmployeeRequiredMixin, TemplateView):
    template_name = "quotations/create_quotation.html"
    success_url = reverse_lazy("dashboard")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        notification = Notification.objects.filter(id=kwargs['pk']).first()
        transport = Transport.objects.filter(id=notification.transport.id).first()

        context["form"] = CreateQuotationForm(initial={'transport': transport})
        return render(request, 'quotations/create_quotation.html', context)

    def post(self, request, *args, **kwargs):
        quotation_form = CreateQuotationForm(request.POST, prefix='quotation')

        if quotation_form.is_valid():
            quotation = quotation_form.save(commit=False)
            return render(request, "quotation_detail.html", {'quotation': quotation})

        return redirect('quotation-create')
