from django.db import models
from cargos import consts as status
from users.models import CustomUser


class CargoTransportStatus(models.Model):
    STATUS_CHOICES = [
                        (status.STATUS_PENDING_ACCEPTANCE, "Pending acceptance"),
                        (status.STATUS_ACCEPTED, "Accepted"),
                        (status.STATUS_IN_PROGRESS, "In progress"),
                        (status.STATUS_COMPLETED, "Completed"),
                        (status.STATUS_REJECTED, "Rejected")
                    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=status.STATUS_PENDING_ACCEPTANCE)

    def __str__(self) -> str:
        return f"Transport demand created at: {self.created_at},last update {self.updated_at}, Status: {self.status}"


class CargoTransport(models.Model):
    """
        The CargoTransport model represents customer cargo pickup and delivery point and price.
        Working in conjunction with OrderDimension for better performance
    """
    cargo_status = models.ForeignKey(CargoTransportStatus, on_delete=models.CASCADE)
    total_distance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Distance", default=1)
    total_duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Duration", default=1)
    transport_distance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Transport Distance", default=1)
    transport_duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Transport Duration", default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    collection_date = models.DateTimeField(auto_now_add=True, verbose_name="Collection Date")
    collection_address = models.CharField(
        max_length=100,
        verbose_name="Collection Address",
        help_text="Collection address",
        default="AZM"
    )
    delivery_address = models.CharField(
        max_length=100,
        verbose_name="Delivery Address",
        help_text="Delivery address",
        default="AZM"
    )

    def __str__(self) -> str:
        return (f""
                f"Cargo {self.id}"
                f"Collection Date: {self.collection_date} "
                f"Collection address: {self.collection_address} "
                f"Delivery address: {self.delivery_address}"
                f"Transport distance: {self.transport_distance} "
                f"Total distance: {self.total_distance}"
                f"Price: {self.price} "

                )


class CargoDimension(models.Model):
    """
    The CargoDimension model represents cargo dimensions it weights.
     With its help will decide what type of vehicle will do CargoTransport.
    """
    cargo = models.OneToOneField(CargoTransport, on_delete=models.CASCADE, verbose_name="Cargo", related_name='dimensions')
    length = models.FloatField(help_text='length of the cargo bed in centimeters', verbose_name="Length", default=1)
    width = models.FloatField(help_text='width  of the cargo bed in centimeters',  verbose_name="Width", default=1)
    height = models.FloatField(help_text='height of the cargo bed in centimeters', verbose_name="Height", default=1)
    weight = models.FloatField(help_text='Gross Vehicle Weight in Kilograms', verbose_name="Weight", default=1)

    def __str__(self):
        return f"Cargo {self.cargo.id} : Weight:{self.weight}, Length:{self.length}, Width:{self.width}, Height:{self.height}"

