import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from airport.models import Country, Airport, Route, AirplaneType, Airplane, Crew, Flight


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


def detail_url(view_name: str, pk: int) -> str:
    return reverse(view_name, args=[pk])


def sample_country(**params) -> Country:
    defaults = {"name": "Test_country"}
    defaults.update(**params)
    return Country.objects.create(**defaults)


def sample_airport(**params) -> Airport:
    defaults = {
        "name": "Test_airport",
        "closest_big_city": "Test_city",
        "country": sample_country(),
    }
    defaults.update(**params)
    return Airport.objects.create(**defaults)


def sample_route(**params) -> Route:
    airport1 = sample_airport()
    airport2 = sample_airport()
    defaults = {
        "source": airport1,
        "destination": airport2,
        "distance": 1234,
    }
    defaults.update(**params)
    return Route.objects.create(**defaults)


def sample_airplane_type(**params) -> AirplaneType:
    defaults = {"name": "Test_type"}
    defaults.update(**params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params) -> Airplane:
    defaults = {
        "name": "Test_airplane",
        "rows": 100,
        "seats_in_row": 10,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(**params)
    return Airplane.objects.create(**defaults)


def sample_crew(**params) -> Crew:
    defaults = {
        "first_name": "Bob",
        "last_name": "Johnson",
    }
    defaults.update(**params)
    return Crew.objects.create(**defaults)


def sample_flight(**params) -> Crew:
    defaults = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": datetime.datetime(2024, 8, 31, 21, 0, 0),
        "arrival_time": datetime.datetime(2024, 8, 31, 22, 0, 0),
    }
    defaults.update(**params)
    flight = Flight.objects.create(**defaults)
    return flight
