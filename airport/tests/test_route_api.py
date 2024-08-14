from django.urls import reverse
from rest_framework import status

from airport.models import Route
from airport.tests.base import (
    BaseSetUp,
    sample_airport,
    sample_route,
    detail_url,
)
from airport.serializers import (
    RouteListSerializer,
    RouteDetailSerializer,
)

ROUTE_URL = reverse("airport:route-list")


class UnauthenticatedRouteAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRouteAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        sample_route()
        sample_route()

        res = self.client.get(ROUTE_URL)

        routes = Route.objects.order_by("id")
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_route(self):
        route = sample_route()

        view_name = "airport:route-detail"

        res = self.client.get(detail_url(view_name, route.id))

        serializer = RouteDetailSerializer(route)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_route_forbidden(self):
        airport1 = sample_airport()
        airport2 = sample_airport()
        payload = {
            "source": airport1.id,
            "destination": airport2.id,
            "distance": 1234,
        }
        res = self.client.post(ROUTE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_route(self):
        airport1 = sample_airport()
        airport2 = sample_airport()
        payload = {
            "source": airport1.id,
            "destination": airport2.id,
            "distance": 1234,
        }
        res = self.client.post(ROUTE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
