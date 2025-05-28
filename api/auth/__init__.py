from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import User, HealthRecord
from api.auth.views import require_patient

class HealthRecordTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="patient1", password="test123")
        self.user.is_patient = True
        self.user.save()
        self.client.force_authenticate(self.user)

        if not hasattr(self.user, "patient_profile"):
            self.user.patient_profile = require_patient(self.user)

        self.record = HealthRecord.objects.create(
            patient=self.user.patient_profile,
            title="Initial Record",
            description="Initial health record content"
        )

    def test_list_health_records(self):
        url = reverse("healthrecord-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_health_record(self):
        url = reverse("healthrecord-list")
        data = {
            "title": "New Record",
            "description": "Description here"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_health_record(self):
        url = reverse("healthrecord-detail", args=[self.record.id])
        response = self.client.put(url, {"title": "Updated Record"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_health_record(self):
        url = reverse("healthrecord-detail", args=[self.record.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
