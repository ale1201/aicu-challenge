from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user profile information.
    Includes custom validation for email uniqueness and password strength.
    """
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "role"]

    def validate_email(self, value):
        """
        Ensure that the email provided is unique among all users.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with that email already exists.")
        return value

    def validate_password(self, value):
        """
        Use Django's built-in password validators to ensure strength.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        return value

    def update(self, instance, validated_data):
        """
        Update user profile fields and optionally change the password.
        """
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
