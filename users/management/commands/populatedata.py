from django.core.management.base import BaseCommand

from users.factories import ClientFactory, DepartmentFactory, EmployeeFactory, EmployeeStatusFactory
from users.models import Client, Employee, EmployeeStatus


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        clients = self.clients_factories()

    @staticmethod
    def clients_factories():
        clients = ClientFactory.create_batch(50,)
        return clients

    @staticmethod
    def employee_factories():
        employees = EmployeeFactory.create_batch(50)
        return employees
