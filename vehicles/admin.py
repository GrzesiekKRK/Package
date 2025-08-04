from django.contrib import admin
from vehicles.models import Vehicle, VehicleDimension


class VehicleAdmin(admin.ModelAdmin):
    list_filter = [
        "type",
        "department"
    ]
    ordering = ["department"]
    search_fields = ["department", "plates", "type"]
    list_per_page = 25


class VehicleDimensionAdmin(admin.ModelAdmin):
    list_filter = ["vehicle",
                   "width",
                   "length",
                   "height",
                   "payload_capacity"
                   ]
    ordering = ["vehicle"]
    list_per_page = 25


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleDimension, VehicleDimensionAdmin)
