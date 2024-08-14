from django.urls import reverse
from rest_framework import status

from airport.models import Order
from airport.tests.base import (
    BaseSetUp,
    detail_url,
    sample_ticket,
    sample_flight,
)
from airport.serializers import (
    OrderDetailSerializer,
    OrderSerializer,
    TicketSerializer,
)

ORDER_URL = reverse("airport:order-list")


class UnauthenticatedOrderAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserOrderAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        order1 = Order.objects.create(user=self.user)
        sample_ticket(order1)
        sample_ticket(order1, seat=2)
        order2 = Order.objects.create(user=self.user)
        sample_ticket(order2)
        sample_ticket(order2)

        res = self.client.get(ORDER_URL)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_detail_order(self):
        order = Order.objects.create(user=self.user)
        sample_ticket(order)
        sample_ticket(order, seat=2)

        view_name = "airport:order-detail"

        res = self.client.get(detail_url(view_name, order.id))

        serializer = OrderDetailSerializer(order)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
