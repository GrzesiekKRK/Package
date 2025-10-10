from django.db import models

from users.models import Department
from vehicles import consts as vehicle_type


class Vehicle(models.Model):
    """
        The Vehicle model represents vehicles (Solo Truck, Tractor, Semi-trailer) operated by a specific company.
        It works in conjunction with the VehicleDimension component to improve overall performance.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, help_text="The department this vehicle belongs to.")
    type = models.CharField(max_length=30, choices=vehicle_type.TRUCK_TYPE_CHOICES, help_text="The type of vehicle.")
    plates = models.CharField(max_length=20, unique=True, help_text="The register plates of the vehicle.")
    connected_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'type': 'tractor'},
        related_name='attached_trailers',
        help_text="The attached semi-trailer.",
    )

    def __str__(self) -> str:
        return f"Vehicle {self.type} with plates number: {self.plates} "

    def clean(self) -> None:
        from django.core.exceptions import ValidationError

        if self.type == "solo_truck" and self.connected_to is not None:
            raise ValidationError("Only Tractor can attach Semi-trailer")
        elif self.type == 'semi-trailer' and self.connected_to is not None:
            raise ValidationError("Cannot attach same type vehicles")


class VehicleDimension(models.Model):
    """
    The VehicleDimension model represents cargo bed dimensions and payload capacity for each vehicle
    """
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='dimensions')
    length = models.FloatField(help_text='length of the cargo bed in centimeters')
    width = models.FloatField(help_text='width  of the cargo bed in centimeters')
    height = models.FloatField(help_text='height of the cargo bed in centimeters')
    payload_capacity = models.FloatField(help_text='Gross Vehicle Weight in Kilograms', verbose_name='GVW')

    def __str__(self):
        return f"Cargo bed of {self.vehicle.type} {self.vehicle.plates}: Payload capacity:{self.payload_capacity}, Length:{self.length}, Width:{self.width}, Height:{self.height}"


