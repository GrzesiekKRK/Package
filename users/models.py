from django.contrib.auth.models import AbstractUser
from django.db import models
from users import consts as departments
from django.utils import timezone
from django.core.exceptions import ValidationError
from icecream import ic

#TODO Factories
class CustomUser(AbstractUser):
    """
        Custom user model extending the base AbstractUser to include additional fields
        specific to the application. This includes role management, user-specific
        information, and secondary contact details.
    """
    email = models.EmailField(max_length=50, unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=11, verbose_name="Phone Number")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)
    secondary_email = models.EmailField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Secondary Email",
        help_text="Emergency email if primary email is lost. Optional",
    )
    billing_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Billing Address",
        help_text="Billing address",
    )
    postal_code = models.CharField(
        max_length=10, verbose_name="Postal Code", default="32-856"
    )

    def save(self, *args, **kwargs):
        self.check_slug()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def check_slug(self):
        if not self.slug:
            number = 1
            slug = f"{self.first_name}-{self.last_name}"
            while CustomUser.objects.filter(slug=slug).exists():
                slug = f"{self.first_name}-{self.last_name}-{number}"
                number += 1
            self.slug = slug


class Department(models.Model):
    """
        The Department model represents office or transport hub for company
    """
    DEPARTMENTS_CHOICES = (
        (departments.OFFICE, "Office"),
        (departments.TRANSPORT, "Transport"),

    )
    type = models.PositiveSmallIntegerField(choices=DEPARTMENTS_CHOICES, default=departments.OFFICE)
    address = models.CharField(max_length=100, unique=True, verbose_name="Building Address")

    def __str__(self) -> str:
        return f"{self.type} {self.address}"


#TODO konto powstaje z randomowym hasłem i wymaganie zmiany po 1 logowaniu
class Employee(CustomUser):
    """
        The Employee model creates info about drivers assigned to transport departments or office employees.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    payroll_account = models.CharField(max_length=26)
    driver = models.BooleanField(default=False)
    driver_semi = models.BooleanField(default=False)
    on_route = models.BooleanField(default=False)
    annual_leave_days = models.PositiveIntegerField(default=26, help_text="Number of annual leave days")

    def __str__(self) -> str:
        return (f""
                f"{self.first_name} {self.last_name}"
                f" department {self.department.type} address {self.department.address}"
                )

    class Meta:
        verbose_name = "Employee"

    def get_available_leave_days(self, year=None):
        """Keep record how many annual leave days are available for employee"""
        if year is None:
            year = timezone.now().year
        used_days = self.annual_leaves.filter(
            start_date__year=year,
            status='approved'
        ).aggregate(
            total=models.Sum('days_count')
        )['total'] or 0
        return self.annual_leave_days - used_days

    def is_available_on_date(self, date):
        """Check is employee is available on date"""
        return not (
                self.annual_leaves.filter(
                    start_date__lte=date,
                    end_date__gte=date,
                    status='approved'
                ).exists() or
                self.sick_leaves.filter(
                    start_date__lte=date,
                    end_date__gte=date
                ).exists()
        )
