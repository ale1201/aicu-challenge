from rest_framework import serializers
from api.models import (
    Annotation,
)


class AnnotationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Annotation model.
    Includes a read-only doctor_name field derived from the related User model.
    """

    doctor_name = serializers.CharField(
        source="doctor.user.get_full_name", read_only=True
    )

    class Meta:
        model = Annotation
        fields = fields = ["doctor_name", "comment", "created_at"]
