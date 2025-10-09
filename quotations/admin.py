from django.contrib import admin
from quotations.models import Quotation, BasePriceModificator


class BasePriceModificatorAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type',)


admin.site.register(Quotation)
admin.site.register(BasePriceModificator, BasePriceModificatorAdmin)



