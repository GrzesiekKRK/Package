from django.db import models

from transports.models import Transport


class Quotation(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    toll_fee = models.FloatField(help_text='Toll Fee', verbose_name="Toll Fee", default=0)
    fuel_cost = models.FloatField(help_text='Fuel Cost', verbose_name="Fuel Cost")
    driver_cost = models.FloatField(help_text='Driver Cost')
    maintenance_cost = models.FloatField(help_text='Truck Maintenance Cost')
    minimal_profit = models.IntegerField(help_text='Minimal profit for this transport')
    total_price = models.FloatField(help_text='Total price for this transport')
