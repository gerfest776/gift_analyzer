from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from villagers.models import Importer, Villager


class TestApi(APITestCase):
    fixtures = ["my_fixture.json"]

    @classmethod
    def setUpTestData(cls):
        cls.post_data = {
            "villagers": [
                {
                    "relatives": [2],
                    "birth_date": "01.01.2003",
                    "citizen_id": 1,
                    "town": "hi",
                    "street": "string",
                    "building": "string",
                    "apartment": 9,
                    "name": "string",
                    "gender": "string",
                },
                {
                    "relatives": [],
                    "birth_date": "01.10.1956",
                    "citizen_id": 2,
                    "town": "hi",
                    "street": "string",
                    "building": "string",
                    "apartment": 9,
                    "name": "sadkadssdg",
                    "gender": "string",
                },
            ]
        }

    def test_create_importer(self):
        url = reverse("importer-list")
        post_data = self.post_data
        response = self.client.post(url, post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"data": {"import_id": 2}})
        self.assertEqual(
            list(
                Importer.objects.filter(import_id=2)
                .first()
                .villagers.values_list("citizen_id", flat=True)
            ),
            [villager["citizen_id"] for villager in post_data["villagers"]],
        )

    def test_patch(self):
        url = reverse("importer-citizens-patch", args=["1", "2"])
        patch_data = {"name": "HelloWorld!"}
        patch_relatives = {"relatives": [4]}
        response = self.client.patch(url, patch_data, format="json")
        # response_relatives = self.client.patch(url, patch_relatives, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Villager.objects.filter(citizen_id=2).first().name, patch_data["name"]
        )
        self.assertEqual(
            list(
                Villager.objects.filter(citizen_id=2)
                .first()
                .relatives.values_list("id", flat=True)
            ),
            patch_relatives["relatives"],
        )

    def test_list(self):
        url = reverse("importer-citizens", args="1")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_birthdays(self):
        url = reverse("importer-citizens-birthdays", args="1")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["1"],
            [{"citizen_id": 2, "presents": 1}, {"citizen_id": 3, "presents": 1}],
        )

    def test_percentile(self):
        url = reverse("importer-citizens-percentile", args="1")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"][0],
            {"town": "Moscow", "p50": [2], "p75": [2], "p99": [3]},
        )
