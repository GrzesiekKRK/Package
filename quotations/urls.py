from django.urls import path
from quotations.views import CreateQuotationView, QuotationDetailView, QuotationListView, QuotationUpdateView, VehiclePriceModificatorCreateView, VehiclePriceModificatorListView, VehiclePriceModificatorDetailView, VehiclePriceModificatorUpdateView


urlpatterns = [
    path("quotations/<int:pk>", CreateQuotationView.as_view(), name="quotation-create"),
    path("quotations/<int:pk>/detail", QuotationDetailView.as_view(), name="quotation-detail"),
    path("quotations/list", QuotationListView.as_view(), name="quotation-list"),
    path("quotations/<int:pk>/update", QuotationUpdateView.as_view(), name="quotation-update"),
    path("quotations/price-modificator/create", VehiclePriceModificatorCreateView.as_view(), name="price-modificator-create"),
    path("quotations/price-modificator/list", VehiclePriceModificatorListView.as_view(), name="price-modificator-list"),
    path("quotations/price-modificator/<int:pk>/detail", VehiclePriceModificatorDetailView.as_view(), name="price-modificator-detail"),
    path("quotations/price-modificator/<int:pk>/update", VehiclePriceModificatorUpdateView.as_view(), name="price-modificator-update"),
]
