from django.urls import reverse
from rest_framework import status

from airport.models import Country
from airport.tests.base import BaseSetUp, sample_country
from airport.serializers import CountrySerializer

COUNTRIES_URL = reverse("airport:country-list")


class UnauthenticatedCountryAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(COUNTRIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCountryAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_countries(self):
        sample_country()
        sample_country()

        res = self.client.get(COUNTRIES_URL)

        countries = Country.objects.order_by("id")
        serializer = CountrySerializer(countries, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_country_with_filter(self):
        country1 = sample_country(name="AAA")
        country2 = sample_country(name="BBB")

        res = self.client.get(COUNTRIES_URL, {"name": "a"})

        serializer1 = CountrySerializer(country1)
        serializer2 = CountrySerializer(country2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_country_forbidden(self):
        payload = {"name": "New Country"}
        res = self.client.post(COUNTRIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCountryAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_country(self):
        payload = {"name": "New Country"}
        res = self.client.post(COUNTRIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
