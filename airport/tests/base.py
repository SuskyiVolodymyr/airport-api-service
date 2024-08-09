from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from airport.models import Country


class BaseSetUp(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.admin = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )


def sample_country(**params):
    defaults = {"name": "Test_country"}
    defaults.update(**params)
    return Country.objects.create(**defaults)
