from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import User, DoctorPatientAssignment, Doctor, Patient

class AssignmentTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.doctor = User.objects.create_user(username="doc", password="pass", email="testd@test.com", role="doctor")
        Doctor.objects.create(user=self.doctor) 
        self.doctor.save()

        self.patient = User.objects.create_user(username="pat", password="pass", email="testp@test.com", role="patient")
        Patient.objects.create(user=self.patient)
        self.patient.save()
        
        self.client.force_authenticate(self.admin)

    def test_prevent_duplicate_assignment(self):
        DoctorPatientAssignment.objects.create(doctor=self.doctor.doctor_profile, patient=self.patient.patient_profile)
        url = reverse("assignments-list")
        data = {"doctor": self.doctor.id, "patient": self.patient.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
