from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import User, HealthRecord, DoctorPatientAssignment, Doctor, Patient

class AnnotationTests(APITestCase):

    def setUp(self):
        self.doctor = User.objects.create_user(username="doc1", password="pass123", email="testd@test.com", role="doctor")
        Doctor.objects.create(user=self.doctor) 
        self.doctor.save()

        self.patient = User.objects.create_user(username="pat1", password="pass123", email="testp@test.com", role="patient")
        Patient.objects.create(user=self.patient) 
        self.patient.save()

        self.patient_profile = self.patient.patient_profile
        self.record = HealthRecord.objects.create(
            patient=self.patient_profile, data="Record Test")

        DoctorPatientAssignment.objects.create(
            doctor=self.doctor.doctor_profile, patient=self.patient_profile
        )

        self.client.force_authenticate(self.doctor)

    def test_create_annotation(self):
        url = reverse("annotations-list", args=[self.record.id]) 
        data = {"comment": "Patient recovering well"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_prevent_unauthorized_annotation(self):
        other_doctor = User.objects.create_user(username="doc2", password="pass",  email="testd2@test.com", role="doctor")
        other_doctor.is_doctor = True
        self.client.force_authenticate(other_doctor)
        url = reverse("annotations-list", args=[self.record.id])
        response = self.client.post(url, {"comment": "New note"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
