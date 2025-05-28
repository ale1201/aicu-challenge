from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser to include user roles
    and enforce email as a required unique identifier.
    """

    ROLE_CHOICES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Patient(models.Model):
    """
    Represents additional patient-specific information.
    Linked via OneToOneField to the custom User model.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    health_insurance_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"


class Doctor(models.Model):
    """
    Represents additional doctor-specific information.
    Linked via OneToOneField to the custom User model.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialties = models.CharField(max_length=255)

    def __str__(self):
        return f"Doctor: {self.user.get_full_name()}"


class HealthRecord(models.Model):
    """
    Represents a health record associated with a patient.
    """

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="records"
    )
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"HealthRecord for {self.patient.user.username} ({self.created_at.date()})"
        )


class DoctorPatientAssignment(models.Model):
    """
    Tracks the assignment relationship between doctors and patients.
    """

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="assigned_patients"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="assigned_doctors"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.user.username} -> {self.patient.user.username}"


class Annotation(models.Model):
    """
    Allows doctors to annotate patient health records.
    """

    record = models.ForeignKey(
        HealthRecord, on_delete=models.CASCADE, related_name="annotations"
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Annotation by {self.doctor.user.username} on {self.record.id}"
