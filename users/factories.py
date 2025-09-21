import random

import factory
# from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker
from users.models import Client, Employee, Department
fake = Faker()


#TODO Change password setter to 'defaultpassword'
class CustomUserFactory(DjangoModelFactory):
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
