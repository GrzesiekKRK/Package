from django.urls import path
from quotations.views import CreateQuotationView, QuotationDetailView, QuotationListView, QuotationUpdateView


urlpatterns = [
    path("quotations/<int:pk>", CreateQuotationView.as_view(), name="quotation-create"),
    path("quotations/<int:pk>/detail", QuotationDetailView.as_view(), name="quotation-detail"),
    path("quotations/list", QuotationListView.as_view(), name="quotation-list"),
    path("quotations/<int:pk>/update", QuotationUpdateView.as_view(), name="quotation-update"),
]
