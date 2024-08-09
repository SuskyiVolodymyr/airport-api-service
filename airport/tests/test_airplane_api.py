import os.path
import tempfile

from PIL import Image
from django.urls import reverse
from rest_framework import status

from airport.models import Airplane
from airport.tests.base import (
    BaseSetUp,
    sample_airplane,
    sample_airplane_type,
)
from airport.serializers import (
    AirplaneListRetrieveSerializer,
)

AIRPLANE_URL = reverse("airport:airplane-list")


class UnauthenticatedAirplaneAPITests(BaseSetUp):
    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAirplaneAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        sample_airplane()

        res = self.client.get(AIRPLANE_URL)

        airplanes = Airplane.objects.order_by("id")
        serializer = AirplaneListRetrieveSerializer(airplanes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_forbidden(self):
        payload = {
            "name": "Test_airplane",
            "rows": 100,
            "seats_in_row": 10,
            "airplane_type": sample_airplane_type().id,
        }
        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_capacity(self):
        airplane = sample_airplane()
        self.assertTrue(hasattr(airplane, "capacity"))
        self.assertEqual(airplane.capacity, airplane.rows * airplane.seats_in_row)


class AdminRouteAPITests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)

    def test_create_route(self):
        payload = {
            "name": "Test_airplane",
            "rows": 100,
            "seats_in_row": 10,
            "airplane_type": sample_airplane_type().id,
        }
        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AirplaneImageUploadTests(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.admin)
        self.airplane = sample_airplane()

    @staticmethod
    def image_upload_url(airplane_id):
        return reverse("airport:airplane-upload-image", args=[airplane_id])

    def test_upload_image_to_airplane(self):
        url = self.image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")

        self.airplane.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.airplane.image.path))

    def test_upload_image_bad_request(self):
        url = self.image_upload_url(self.airplane.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_airplane_list_should_not_work(self):
        url = AIRPLANE_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "name": "New_test_airplane",
                    "rows": 100,
                    "seats_in_row": 10,
                    "airplane_type": sample_airplane_type().id,
                    "image": ntf,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.get(name="New_test_airplane")
        self.assertFalse(airplane.image)

    def test_image_url_is_shown_on_airplane_list(self):
        url = self.image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(AIRPLANE_URL)

        self.assertIn("image", res.data[0].keys())
