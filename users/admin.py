from django.contrib import admin

from .models import CustomUser, Client, Department, Employee, EmployeeStatus


class ClientAdmin(admin.ModelAdmin):
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
    search_fields = ["type", "address"]
    ordering = ["type"]
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
                    "task_in_progress",
                    "annual_leave_days_total",
                    "annual_leave_days_used",
                    "presence_status",
                    "absence_days",
                    "annual_leave_start",
                    "annual_leave_end",
                    "medical_leave_days",
                    "medical_leave_start",
                    "medical_leave_end",
                    "years_of_work",
                    ]
    search_fields = ["task_in_progress",  "annual_leave_days_used", "presence_status", "annual_leave_start", "annual_leave_end",  "absence_days", "medical_leave_start", "medical_leave_days", "medical_leave_end",]
    ordering = ["presence_status"]
    list_per_page = 25


admin.site.register(Client, ClientAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeStatus, EmployeeStatusAdmin)
admin.site.register(CustomUser)
