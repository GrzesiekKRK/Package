from django.views.generic import UpdateView, DetailView, ListView, TemplateView
from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from quotations.forms import CreateQuotationForm, UpdateQuotationForm, CreateBasePriceModificatorForm
from quotations.models import Quotation, BasePriceModificator
from users.permission import EmployeeRequiredMixin
from notifications.models import Notification
from notifications.views import CreateNotification
from transports.models import Transport, TransportStatus
from users.models import Client
from icecream import ic


class CreateQuotationView(EmployeeRequiredMixin, TemplateView):
    template_name = "quotations/create_quotation.html"
    success_url = reverse_lazy("dashboard")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        notification = Notification.objects.filter(id=kwargs['pk']).first()

        transport_id = int(notification.title)
        transport = Transport.objects.filter(id=transport_id).first()

        context["form"] = CreateQuotationForm(initial={'transport': transport})
        return render(request, 'quotations/create_quotation.html', context)

    #TODO powiadomienie dla klienta z ceną
    def post(self, request, *args, **kwargs):
        quotation_form = CreateQuotationForm(request.POST)
        if quotation_form.is_valid():

            quotation = quotation_form.save()
            transport = quotation.transport.transport_status.id
            transport_status = TransportStatus.objects.filter(id=transport).first()
            transport_status.status = 2
            transport_status.save()
            user = transport_status.user
            ic(quotation)
            CreateNotification.client_quotation_notification(user=user, quotation=quotation)
            return redirect("quotation-detail", pk=quotation.id)

        return redirect('dashboard')


#TODO wyszukiwanie po id transportu lub wyceny
class QuotationListView(EmployeeRequiredMixin, ListView):
    model = Quotation
    template_name = "quotations/quotation_list.html"


class QuotationDetailView(EmployeeRequiredMixin, DetailView):
    model = Quotation
    template_name = "quotations/quotation_detail.html"


#TODO nadpisać get aby pobrac numer transportu
class QuotationUpdateView(EmployeeRequiredMixin, UpdateView):
    model = Quotation
    template_name = "quotations/quotation_update.html"
    form_class = UpdateQuotationForm
    success_url = reverse_lazy("quotation-list")

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            kwargs["transport"] = self.object.transport.id
        return super().get_context_data(**kwargs)
