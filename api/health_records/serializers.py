from rest_framework import serializers
from api.annotations.serializers import AnnotationSerializer
from api.models import HealthRecord


class HealthRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the HealthRecord model.
    Includes related annotations as a nested read-only field.
    """

    annotations = AnnotationSerializer(many=True, read_only=True)

    class Meta:
        model = HealthRecord
        fields = ["id", "data", "created_at", "updated_at", "annotations"]
