from django.urls import path
from cargos.views import CreateCargoTransport

urlpatterns = [
    path("cargo/create/", CreateCargoTransport.create_cargo, name="create_cargo"),
]
