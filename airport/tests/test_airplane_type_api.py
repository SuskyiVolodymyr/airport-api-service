from django.urls import reverse
from rest_framework import status

from airport.models import AirplaneType
from airport.tests.base import BaseSetUp, sample_airplane_type
from airport.serializers import AirplaneTypeSerializer

AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


class UnauthenticatedAirplaneTypeAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAirplaneTypeAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_airplane_types(self):
        sample_airplane_type()
        sample_airplane_type()

        res = self.client.get(AIRPLANE_TYPE_URL)

        airplane_types = AirplaneType.objects.order_by("id")
        serializer = AirplaneTypeSerializer(airplane_types, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_type_forbidden(self):
        payload = {"name": "New Airplane Type"}
        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_country(self):
        payload = {"name": "New Airplane Type"}
        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
