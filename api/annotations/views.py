from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response

from api.models import Annotation, HealthRecord, DoctorPatientAssignment
from .serializers import AnnotationSerializer
from api.auth.views import require_doctor


class AnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle annotations made by doctors on patient health records.

    Permissions:
        - Only authenticated doctors can perform actions.
        - Doctors can only annotate records of their assigned patients.
        - Doctors can only modify/delete their own annotations.

    Endpoints:
        - GET /annotations/
        - POST /records/{record_id}/annotations/
        - PUT /annotations/{id}/
        - DELETE /annotations/{id}/
    """

    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter annotations to those created by the authenticated doctor.

        Returns:
            QuerySet of Annotation objects.
        """
        doctor = require_doctor(self.request.user)
        return Annotation.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        """
        Create a new annotation on a health record.

        - Ensures the doctor is assigned to the patient whose record is being annotated.
        - Raises 403 if doctor is not assigned to that patient.
        """
        doctor = require_doctor(self.request.user)
        record_id = self.kwargs.get("record_id")

        if not record_id:
            raise ValidationError({"record_id": "'record_id' parameter is missing."})

        try:
            record = HealthRecord.objects.select_related("patient").get(pk=record_id)
        except HealthRecord.DoesNotExist:
            raise NotFound("Health record not found.")

        if not DoctorPatientAssignment.objects.filter(doctor=doctor, patient=record.patient).exists():
            raise PermissionDenied("You are not assigned to this patient.")

        serializer.save(doctor=doctor, record=record)

    def update(self, request, *args, **kwargs):
        """
        Update an annotation.

        - Allowed only if the annotation was made by the current doctor.
        """
        annotation = self.get_object()
        if annotation.doctor != require_doctor(request.user):
            raise PermissionDenied("You can only update your own annotations.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an annotation.

        - Allowed only if the annotation was made by the current doctor.
        """
        annotation = self.get_object()
        if annotation.doctor != require_doctor(request.user):
            raise PermissionDenied("You can only delete your own annotations.")
        return super().destroy(request, *args, **kwargs)
