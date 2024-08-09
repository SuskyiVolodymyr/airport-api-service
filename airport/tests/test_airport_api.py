from django.urls import reverse
from rest_framework import status

from airport.models import Airport
from airport.tests.base import BaseSetUp, sample_airport, sample_country
from airport.serializers import AirportListSerializer

AIRPORT_URL = reverse("airport:airport-list")


class UnauthenticatedAirportAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAirportAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        sample_airport()
        sample_airport()

        res = self.client.get(AIRPORT_URL)

        airports = Airport.objects.order_by("id")
        serializer = AirportListSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_airports_with_filter_by_name(self):
        airport1 = sample_airport(name="AAA")
        airport2 = sample_airport(name="BBB")

        res = self.client.get(AIRPORT_URL, {"name": "a"})

        serializer1 = AirportListSerializer(airport1)
        serializer2 = AirportListSerializer(airport2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "Test_airport",
            "closest_big_city": "Test_city",
            "country": sample_country().id,
        }
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCountryAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_airport(self):
        payload = {
            "name": "Test_airport",
            "closest_big_city": "Test_city",
            "country": sample_country().id,
        }
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
