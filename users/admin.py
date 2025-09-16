from django.contrib import admin

from .models import CustomUser, Department, Employee, EmployeeStatus


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "date_joined",
    ]
    list_filter = ["is_active", "date_joined"]
    ordering = ["-date_joined"]
    search_fields = ["email", "username", "first_name", "last_name"]
    list_per_page = 25


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["address"]
    list_per_page = 25


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
                    "first_name",
                    "last_name",
                    "department",
                    "driver",
                    "driver_semi",

                ]
    search_fields = ["department", "driver", "driver_semi"]
    ordering = ["department"]
    list_per_page = 25


class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = [
                    "on_route",
                    "annual_leave_days_total",
                    "annual_leave_days_used",
                    "absence_status",
                    "absence_days",
                    "sick_leaves_days_taken",
                    "sick_leaves_days"
                    ]
    search_fields = ["on_route",  "annual_leave_days_used", "absence_status", "absence_days", "sick_leaves_days_taken", "sick_leaves_days",]
    ordering = ["absence_status"]
    list_per_page = 25


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeStatus, EmployeeStatusAdmin)
