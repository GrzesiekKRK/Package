from django.urls import path
from quotations.views import CreateQuotationView, QuotationDetailView, QuotationListView, QuotationUpdateView, VehiclePriceModificatorCreateView, VehiclePriceModificatorListView, VehiclePriceModificatorDetailView, VehiclePriceModificatorUpdateView


urlpatterns = [
    path("<int:pk>", CreateQuotationView.as_view(), name="quotation-create"),
    path("<int:pk>/detail", QuotationDetailView.as_view(), name="quotation-detail"),
    path("list", QuotationListView.as_view(), name="quotation-list"),
    path("update", QuotationUpdateView.as_view(), name="quotation-update"),
    path("price-modificator/create", VehiclePriceModificatorCreateView.as_view(), name="price-modificator-create"),
    path("price-modificator/list", VehiclePriceModificatorListView.as_view(), name="price-modificator-list"),
    path("price-modificator/<int:pk>/detail", VehiclePriceModificatorDetailView.as_view(), name="price-modificator-detail"),
    path("price-modificator/<int:pk>/update", VehiclePriceModificatorUpdateView.as_view(), name="price-modificator-update"),
]
