from django.core.management.base import BaseCommand

from users.factories import ClientFactory
from users.models import Client, Employee, EmployeeStatus


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        users = self.users_factories()

    @staticmethod
    def users_factories():
        users = ClientFactory.create_batch(50,)
        return users

