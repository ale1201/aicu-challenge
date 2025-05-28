from rest_framework import serializers
from api.models import DoctorPatientAssignment


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the DoctorPatientAssignment model.
    Includes read-only fields for displaying the names of the doctor and patient.
    """

    doctor_name = serializers.CharField(
        source="doctor.user.get_full_name", read_only=True
    )
    patient_name = serializers.CharField(
        source="patient.user.get_full_name", read_only=True
    )

    class Meta:
        model = DoctorPatientAssignment
        fields = "__all__"
