from django.urls import path
from quotations.views import CreateQuotationView


urlpatterns = [
    path("<int:pk>/quotation", CreateQuotationView.as_view(), name="quotation-create"),
    path("<int:pk>/quotation/detail", CreateQuotationView.as_view(), name="quotation-detail"),
]
