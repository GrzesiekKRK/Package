from django.core.management.base import BaseCommand

from users.models import Department
from users.factories import ClientFactory, DepartmentFactory, EmployeeFactory, EmployeeStatusFactory
from users.consts import TRANSPORT


class Command(BaseCommand):
    """Create 50 clients, 5 departments and 5 employees par department"""
    def handle(self, *args, **options) -> None:
        self.clients_factories()
        departments = self.departments_factories()
        self.employees_factories(departments)

    @staticmethod
    def clients_factories():
        """Create 50 clients"""
        ClientFactory.create_batch(50,)
        ClientFactory.create(username='ad', is_staff=True, is_superuser=True)

    @staticmethod
    def departments_factories():
        """Create 5 departments"""
        DepartmentFactory.create(address='Office Kraków', type=1)
        DepartmentFactory.create_batch(5, type=2)
        departments = Department.objects.all()
        return departments

    @staticmethod
    def employees_factories(departments):
        """Create 5 employees par department"""
        for department in departments:
            if department.type == TRANSPORT:
                EmployeeFactory.create_batch(5, department=department, driver=True, driver_semi=True)

            EmployeeFactory.create_batch(5, department=department)
