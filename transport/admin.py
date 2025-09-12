from django.contrib import admin

from transport.models import TransportStatus, Transport, CargoDimension


class TransportStatusAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    list_per_page = 25
    ordering = ["-status"]


class TransportAdmin(admin.ModelAdmin):
    list_filter = [
        "collection_date",
        "collection_address",
        "delivery_address",
        "transport_duration"
    ]
    list_per_page = 25
    ordering = ["-collection_date"]


class CargoDimensionAdmin(admin.ModelAdmin):
    list_filter = [
                    "transport",
                    "length",
                    "width",
                    "height",
                    "weight",
                    ]
    ordering = ["transport"]
    list_per_page = 25


admin.site.register(TransportStatus, TransportStatusAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(CargoDimension, CargoDimensionAdmin)
