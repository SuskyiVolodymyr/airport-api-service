import datetime

from django.urls import reverse
from rest_framework import status

from airport.models import Flight
from airport.tests.base import (
    BaseSetUp,
    sample_flight,
    detail_url,
    sample_route,
    sample_airplane,
    sample_crew,
)
from airport.serializers import (
    FlightListSerializer,
    FlightDetailSerializer,
)

FLIGHT_URL = reverse("airport:flight-list")


class UnauthenticatedFlightAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserFlightAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        sample_flight()
        sample_flight()

        res = self.client.get(FLIGHT_URL)

        flights = Flight.objects.order_by("id")
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_flight(self):
        flight = sample_flight()

        view_name = "airport:flight-detail"

        res = self.client.get(detail_url(view_name, flight.id))

        serializer = FlightDetailSerializer(flight)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_flights_by_departure(self):
        flight1 = sample_flight(departure_time=datetime.datetime(2024, 8, 25, 21, 0, 0))
        flight2 = sample_flight(departure_time=datetime.datetime(2024, 9, 25, 21, 0, 0))
        flight3 = sample_flight(
            departure_time=datetime.datetime(2024, 10, 25, 21, 0, 0)
        )

        res = self.client.get(FLIGHT_URL, {"departure": "2024-09-01"})

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)
        self.assertNotIn(serializer1.data, res.data)

    def test_filter_flights_by_arrival(self):
        flight1 = sample_flight(arrival_time=datetime.datetime(2024, 8, 25, 21, 0, 0))
        flight2 = sample_flight(arrival_time=datetime.datetime(2024, 9, 25, 21, 0, 0))
        flight3 = sample_flight(arrival_time=datetime.datetime(2024, 10, 25, 21, 0, 0))

        res = self.client.get(FLIGHT_URL, {"arrival": "2024-10-01"})

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_create_flight_forbidden(self):
        payload = {
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": "2024-08-31 20:00:00",
            "arrival_time": "2024-08-31 21:00:00",
        }
        res = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_flight(self):
        payload = {
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": "2024-08-31 20:00:00",
            "arrival_time": "2024-08-31 21:00:00",
        }
        res = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
