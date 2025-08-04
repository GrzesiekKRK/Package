from django.db import models
from users.models import Department, Employee
from vehicles.models import Vehicle
from cargos.models import CargoTransport, CargoTransportStatus


class Schedule(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    cargo = models.ForeignKey(CargoTransport, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    driver = models.OneToOneField(Employee, on_delete=models.CASCADE)
    status = models.ForeignKey(CargoTransportStatus, on_delete=models.CASCADE)
    collection_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    transport_duration = models.FloatField()
    total_duration = models.FloatField()

    def __str__(self) -> str:
        return f"Schedule {self.cargo} - {self.department} - {self.collection_date}"
