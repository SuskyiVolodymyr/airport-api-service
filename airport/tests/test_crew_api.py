from django.urls import reverse
from rest_framework import status

from airport.models import Crew
from airport.tests.base import (
    BaseSetUp,
    sample_crew,
)
from airport.serializers import CrewSerializer

CREW_URL = reverse("airport:crew-list")


class UnauthenticatedCrewAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCrewAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_crew_members(self):
        sample_crew()
        sample_crew()

        res = self.client.get(CREW_URL)

        crew_members = Crew.objects.order_by("id")
        serializer = CrewSerializer(crew_members, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_crew_member_forbidden(self):
        payload = {
            "first_name": "Bob",
            "last_name": "Johnson",
        }
        res = self.client.post(CREW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_full_name(self):
        crew = sample_crew()
        self.assertTrue(hasattr(crew, "full_name"))
        self.assertEqual(crew.full_name, f"{crew.first_name} {crew.last_name}")


class AdminRouteAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_crew(self):
        payload = {
            "first_name": "Bob",
            "last_name": "Johnson",
        }
        res = self.client.post(CREW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
