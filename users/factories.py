import random
from datetime import datetime, timedelta

import factory
# from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker
from users.models import Client, Department, Employee, EmployeeStatus
from users.consts import DEPARTMENTS
fake = Faker()


def generate_period() -> str:
    """Generate leave period"""
    start_date = fake.date_between(start_date='-1y', end_date='today')
    duration = random.randint(1, 30)  # 1-30 dni zwolnienia
    end_date = start_date + timedelta(days=duration)

    return f"{start_date.strftime('%d/%m/%y')}-{end_date.strftime('%d/%m/%y')}"


#TODO Change password setter to 'defaultpassword'
class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        django_get_or_create = ('username',)

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    secondary_email = factory.Faker("email")
    billing_address = factory.Faker("address")
    password = factory.PostGenerationMethodCall('set_password', 'ad')
    created_at = factory.Faker("date_time_this_decade")
    phone_number = factory.LazyFunction(
                                        lambda: "".join(str(random.randint(0, 9)) for _ in range(9))
                                        )
    postal_code = factory.LazyFunction(
                                        lambda: f"{random.randint(10, 99)}-{random.randint(100, 999)}"
                                        )


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    type = factory.LazyFunction(lambda: random.choice(DEPARTMENTS))
    address = factory.Faker("address")


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    department = factory.SubFactory(DepartmentFactory)


class EmployeeStatusFactory(DjangoModelFactory):
    class Meta:
        model = EmployeeStatus

    employee = factory.SubFactory(EmployeeFactory)
    annual_leave_days_used = factory.LazyFunction(lambda: random.randint(0, 26))
    absence_days = factory.LazyFunction(lambda: random.randint(0, 10))
    annual_leave_period = factory.LazyFunction(generate_period)
    medical_leave_days = factory.LazyFunction(lambda: random.randint(0, 10))
    medical_leave_period = factory.LazyFunction(generate_period)
