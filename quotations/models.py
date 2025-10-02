from django.db import models

from transports.models import Transport


class Quotation(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    kilometer_rate = models.DecimalField(help_text='Kilograms', decimal_places=2, max_digits=6, verbose_name="Cost", default=4.2)
    toll_fee = models.DecimalField(help_text='Toll Fee', decimal_places=2, max_digits=6,  verbose_name="Toll Fee", default=0)
    fuel_cost = models.DecimalField(help_text='Fuel Cost', decimal_places=2, max_digits=6, verbose_name="Fuel Cost")
    driver_rate = models.DecimalField(help_text='Driver Cost', decimal_places=2, max_digits=6, default=0.90)
    maintenance_cost = models.DecimalField(help_text='Truck Maintenance Cost', decimal_places=2, max_digits=6, default=50)
    minimal_profit = models.IntegerField(help_text='Minimal profit for this transport', default=100)
    total_price = models.DecimalField(help_text='Total price for this transport with profit', decimal_places=2, max_digits=6)
