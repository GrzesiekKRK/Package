from django.urls import path
from quotations.views import CreateQuotationView, QuotationDetailView, QuotationListView


urlpatterns = [
    path("<int:pk>/quotation", CreateQuotationView.as_view(), name="quotation-create"),
    path("<int:pk>/quotation/detail", QuotationDetailView.as_view(), name="quotation-detail"),
    path("quotation/list", QuotationListView.as_view(), name="quotation-list"),
]
