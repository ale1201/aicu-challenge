from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import DoctorPatientAssignment
from .serializers import AssignmentSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage doctor-patient assignments.

    Permissions:
        - Only admin users can create, view, or delete assignments.

    Endpoints:
        - GET /assignments/
        - POST /assignments/
        - DELETE /assignments/{id}/
    """

    queryset = DoctorPatientAssignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        """
        Prevent duplicate doctor-patient assignments.

        Raises:
            ValidationError: if the same doctor is already assigned to the patient.
        """
        doctor = serializer.validated_data.get("doctor")
        patient = serializer.validated_data.get("patient")

        if DoctorPatientAssignment.objects.filter(doctor=doctor, patient=patient).exists():
            raise ValidationError("This doctor is already assigned to this patient.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Delete a doctor-patient assignment.

        Returns:
            200 OK with a confirmation message on success.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Assignment deleted successfully"}, status=status.HTTP_200_OK)
