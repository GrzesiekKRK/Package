from django.db import models
from decimal import Decimal
from transports.models import Transport
from vehicles.models import Vehicle
from vehicles import consts as vehicle_type


class BasePriceModificator(models.Model):
    vehicle_type = models.CharField(max_length=30, choices=vehicle_type.TRUCK_TYPE_CHOICES)
    value = models.DecimalField(decimal_places=2, max_digits=6, help_text='Value of modificator for base price tag of solo-truck transport.')

#TODO js sricpt do przeliczania
#TODO Updateview do wybierania pojazdu i po update przeliczania ceny
class Quotation(models.Model):
    """Represents a quotation."""
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    kilometer_rate = models.DecimalField(help_text='Kilograms', decimal_places=2, max_digits=6, verbose_name="Cost", default=4.2)
    toll_fee = models.DecimalField(help_text='Toll Fee', decimal_places=2, max_digits=6,  verbose_name="Toll Fee", default=0)
    fuel_consumption = models.DecimalField(help_text='Fuel rate for 100 kilometers ', decimal_places=2, max_digits=6, default=16.0)
    driver_rate = models.DecimalField(help_text='Driver rate per kilometer', decimal_places=2, max_digits=6, default=0.90)
    maintenance_rate = models.DecimalField(help_text='Truck maintenance cost per transport', decimal_places=2, max_digits=6, default=50)
    minimal_profit = models.IntegerField(help_text='Minimal profit for this transport', default=100)
    total_price = models.DecimalField(help_text='Total price for this transport with profit', decimal_places=2, max_digits=6, default=1100)

    def __str__(self) -> str:
        return f"Quotation for transport number {self.transport.id} with total price: {self.total_price}"

    def driver_cost(self):
        """Calculate driver cost by multiplying driver kilometer rate by total distance covered.Rounded to 2 decimal places."""
        driver_cost = round(self.driver_rate * self.transport.total_distance, 2)
        return driver_cost

    def fuel_cost(self):
        """Calculate fuel cost. Divide the distance by 100 and multiply by fuel consumption. Rounded to 2 decimal places."""
        division = round(self.transport.total_distance / 100, 2)
        fuel_cost = round(self.fuel_consumption * division, 2)
        return fuel_cost

    def voyage_cost(self):
        """Calculate toll fees, fuel, driver, maintenance cost and add distance travel * kilometer rate. Rounded to 2 decimal places."""
        driver_cost = self.driver_cost()
        fuel_cost = self.fuel_cost()
        voyage_cost = round(self.toll_fee + fuel_cost + driver_cost + self.maintenance_rate, 2)
        return voyage_cost

    def calculate_total_price(self):
        """Add voyage cost and minimal profit. Multiply depending on vehicle typ. Rounded to 2 decimal places."""
        voyage_cost = self.voyage_cost()
        truck_type = self.vehicle.type
        modificator = BasePriceModificator.objects.get(vehicle_type=truck_type)
        price = (voyage_cost + self.minimal_profit) * modificator.value
        total_price = round(price, 2)
        return total_price



