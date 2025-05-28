from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound

from api.models import HealthRecord
from .serializers import HealthRecordSerializer
from api.permissions import IsPatientOwner
from api.auth.views import require_patient


class HealthRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations for health records.

    - Patients can create, view, update, and delete **only their own** records.
    - Doctors can view records of their **assigned patients**.
    """

    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter health records based on user type:
        - Patients see their own records.
        - Doctors see records of assigned patients.
        - Others get nothing.
        """
        user = self.request.user

        if hasattr(user, "patient_profile"):
            return HealthRecord.objects.filter(patient=user.patient_profile)

        if hasattr(user, "doctor_profile"):
            assigned_patients = user.doctor_profile.assigned_patients.values_list("patient", flat=True)
            return HealthRecord.objects.filter(patient__in=assigned_patients)

        return HealthRecord.objects.none()

    def perform_create(self, serializer):
        """
        Assigns the authenticated patient to the new health record.
        """
        patient = require_patient(self.request.user)
        serializer.save(patient=patient)

    def update(self, request, *args, **kwargs):
        """
        Updates a health record if the authenticated user owns it.
        """
        record = self._get_owned_record_or_403()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a health record if the authenticated user owns it.
        """
        record = self._get_owned_record_or_403()
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        """
        Adds custom permission `IsPatientOwner` for modifying or deleting records.
        """
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsPatientOwner()]
        return [permissions.IsAuthenticated()]

    def _get_owned_record_or_403(self):
        """
        Internal helper to fetch a health record by `pk` and validate ownership.
        Raises:
            - ValidationError: if `pk` is missing
            - NotFound: if record does not exist
            - PermissionDenied: if user does not own the record
        """
        record_id = self.kwargs.get("pk")
        if not record_id:
            raise ValidationError({"detail": "'pk' parameter is missing."})

        try:
            record = HealthRecord.objects.get(pk=record_id)
        except (ValueError, TypeError, HealthRecord.DoesNotExist):
            raise NotFound("Health record not found.")

        patient = require_patient(self.request.user)
        if record.patient != patient:
            raise PermissionDenied("You can only manage your own records.")

        return record
