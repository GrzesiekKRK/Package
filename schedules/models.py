from django.db import models
from django.core.exceptions import ValidationError
from users.models import Department, Employee
from vehicles.models import Vehicle
from transport.models import Transport, TransportStatus


#TODO Połączyć dyspozycjyność, Spedycja
class Schedule(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Transport, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    driver = models.OneToOneField(Employee, on_delete=models.CASCADE)
    status = models.ForeignKey(TransportStatus, on_delete=models.CASCADE)
    collection_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    transport_duration = models.FloatField()
    total_duration = models.FloatField()

    def __str__(self) -> str:
        return f"Schedule {self.cargo} - {self.department} - {self.collection_date}"


#TODO widok update tylko
class AnnualLeave(models.Model):
    """Annual Leave model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='annual_leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    days_count = models.PositiveIntegerField(help_text="Number of working days of leave")
    reason = models.TextField(blank=True, help_text="Reason for leave (optional)")
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    approved_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be later than end date")

    def __str__(self):
        return f"{self.employee} - leave from {self.start_date} to {self.end_date}"

    class Meta:
        verbose_name = "Annual Leave"
        verbose_name_plural = "Annual Leaves"
        ordering = ['-start_date']


#TODO tylko dla office wgląd
class SickLeave(models.Model):
    """Model for medical sick leave"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sick_leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    days_count = models.PositiveIntegerField(help_text="Number of sick leave days")

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be later than end date")

    def __str__(self):
        return f"{self.employee} - sick leave from {self.start_date} to {self.end_date}"

    class Meta:
        verbose_name = "Sick Leave"
        verbose_name_plural = "Sick Leaves"
        ordering = ['-start_date']
