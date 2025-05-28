from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from api.models import User, Patient, Doctor


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user (patient or doctor).
    Validates email uniqueness and password strength.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "role"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write_only": True}
        }

    def validate_email(self, value):
        """
        Ensure that the email provided is unique across all users.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with that email already exists.")
        return value

    def validate_password(self, value):
        """
        Use Django's password validator.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """
        Create user and attach a corresponding patient or doctor profile.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user.role == "patient":
            Patient.objects.create(user=user)
        elif user.role == "doctor":
            Doctor.objects.create(user=user)

        return user
