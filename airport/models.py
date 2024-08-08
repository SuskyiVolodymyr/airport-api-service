from django.conf import settings
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, related_name="airports", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, related_name="source_routes", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport, related_name="destination_routes", on_delete=models.CASCADE
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, related_name="airplanes", on_delete=models.CASCADE
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Flight(models.Model):
    route = models.ForeignKey(Route, related_name="flights", on_delete=models.CASCADE)
    airplane = models.ForeignKey(
        Airplane, related_name="flights", on_delete=models.CASCADE
    )
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return f"{self.route} {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.created_at

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, related_name="tickets", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("row", "seat", "flight")

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )
