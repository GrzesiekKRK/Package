from django.contrib import admin

from schedules.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_filter = [
                    "collection_date",
                    "delivery_date",
                    "transport_duration",
                    "department",
                    "total_duration",
                    ]
    ordering = ["collection_date"]
    list_per_page = 25


admin.site.register(Schedule, ScheduleAdmin)
