from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Crew,
    Country,
    Flight,
    Order,
    Route,
    Ticket,
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly

from airport.serializers import (
    CountrySerializer,
    AirportSerializer,
    RouteDetailSerializer,
    RouteSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    FlightDetailSerializer,
    FlightSerializer,
    OrderDetailSerializer,
    OrderSerializer,
    RouteListSerializer,
    AirplaneListRetrieveSerializer,
    FlightListSerializer,
)


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    queryset = Country.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name", type=str, description="Filter by name (ex. ?name=abc)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirportViewSet(ModelViewSet):
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    queryset = Airport.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        country = self.request.query_params.get("country")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if country:
            queryset = queryset.filter(country__name__icontains=country)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name", type=str, description="Filter by name (ex. ?name=abc)"
            ),
            OpenApiParameter(
                name="country",
                type=str,
                description="Filter by country (ex. ?name=abc)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        elif self.action == "list":
            return RouteListSerializer
        return RouteSerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListRetrieveSerializer
        return AirplaneSerializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = self.queryset

        departure = self.request.query_params.get("departure")
        arrival = self.request.query_params.get("arrival")

        if departure:
            queryset = queryset.filter(departure_time__gt=departure)
        if arrival:
            queryset = queryset.filter(arrival_time__lt=arrival)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        elif self.action == "list":
            return FlightListSerializer
        return FlightSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="departure",
                type=OpenApiTypes.DATE,
                description="Filter by greater date (ex. ?departure=2024-08-01T19:00:00)",
            ),
            OpenApiParameter(
                name="arrival",
                type=OpenApiTypes.DATE,
                description="Filter by less date (ex. ?arrival=2024-08-01T19:00:00)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        user_id = self.request.query_params.get("user")
        if user_id:
            queryset = queryset.filter(user__id=user_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type=int,
                description="Filter by user id (ex. ?user=1). Only for stuff",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
