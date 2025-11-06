from django.contrib import admin
from quotations.models import Quotation, VehiclePriceModificator


class VehiclePriceModificatorAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type',)


admin.site.register(Quotation)
admin.site.register(VehiclePriceModificator, VehiclePriceModificatorAdmin)



