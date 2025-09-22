from django.contrib.auth.models import AbstractUser
from django.db import models
from users import consts as departments
from django.utils import timezone


class CustomUser(AbstractUser):
    """
            'CustomUser model' extending the base AbstractUser to include additional fields
            specific to the application. This includes user-specific information and secondary contact details.
        """
    email = models.EmailField(max_length=50, unique=True, verbose_name="Email", help_text="Primary contact email use to create user account")
    phone_number = models.CharField(max_length=11, verbose_name="Phone Number", help_text="Contact phone number")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


#TODO Factories
class Client(CustomUser):
    """
        'Client model' is a customer class created to keep an avenue to extend CustomUser
         without making changes to 'Employee model'.
    """
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
        help_text="Billing address ",
    )
    postal_code = models.CharField(
        max_length=10, verbose_name="Postal Code", default="32-856"
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def save(self, *args, **kwargs):
        self.slug = self.username
        super().save(*args, **kwargs)


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
        The Employee model extends 'Person model' and stores info are they drivers assigned to transport departments or office employees.
        Keep payroll account.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, help_text="Office or Garage in which employee will work")
    driver = models.BooleanField(default=False, help_text="Driver License Category 'C'")
    driver_semi = models.BooleanField(default=False, help_text="Driver License Category 'CE")

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


#TODO daty okresu nieobecności
#TODO Forma
class EmployeeStatus(models.Model):
    """'EmployeeStatus model' keep track is employee available how many annual leave days are left or are they on medical leaves or transportin something now"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task_in_progress = models.BooleanField(default=False, help_text="Working on current task")
    annual_leave_days_total = models.PositiveIntegerField(null=True, default=20, help_text="Number of annual leave days")
    annual_leave_days_used = models.PositiveIntegerField(default=0, help_text="Number of annual leave days used")
    annual_leave_start = models.DateTimeField(null=True, blank=True, help_text="Start date of annual leave period")
    annual_leave_end = models.DateTimeField(null=True, blank=True, help_text="End date of annual leave period")
    presence_status = models.BooleanField(default=True, help_text='Is employee available at given date')
    absence_days = models.PositiveIntegerField(default=0, help_text="Number of absence days this year")
    medical_leave_days = models.PositiveIntegerField(default=0, help_text="Number of working days in medical leave period given by doctor")
    medical_leave_start = models.CharField(null=True, max_length=20, help_text="Period of medical leave start date")
    medical_leave_end = models.CharField(null=True, max_length=20, help_text="Period of medical leave end date")
    years_of_work = models.PositiveIntegerField(default=0, help_text="Number of years of work for annual leave counting")

    class Meta:
        verbose_name_plural = "Employee Status"

    def annual_leave_days_count(self) -> None:
        """Count leaves days base on years of work"""

        years = self.years_of_work
        if years < 10:
            self.annual_leave_days_total = 20
        else:
            self.annual_leave_days_total = 26
