from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


# ────────────────
# Utility Functions
# ────────────────

def require_patient(user):
    """
    Ensure the user has an associated patient profile.

    Raises:
        PermissionDenied: If the user is not a patient.
    Returns:
        PatientProfile instance
    """
    if not hasattr(user, 'patient_profile'):
        raise PermissionDenied("User does not have patient permissions.")
    return user.patient_profile


def require_doctor(user):
    """
    Ensure the user has an associated doctor profile.

    Raises:
        PermissionDenied: If the user is not a doctor.
    Returns:
        DoctorProfile instance
    """
    if not hasattr(user, 'doctor_profile'):
        raise PermissionDenied("User does not have doctor permissions.")
    return user.doctor_profile


# ────────────────
# API Views
# ────────────────

class RegisterView(APIView):
    """
    POST /auth/register/
    ---------------------
    Register a new user with optional patient or doctor role.

    Request body:
        - username
        - email
        - password
        - role or profile information

    Returns:
        201 Created on success
        400 Bad Request on validation failure
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /auth/logout/
    -------------------
    Logout the current user by blacklisting the provided refresh token.

    Request body:
        - refresh (JWT token string)

    Permissions:
        - Requires authentication

    Returns:
        205 Reset Content on success
        400 Bad Request on error
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            raise ValidationError({"refresh": "Refresh token is required."})

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )
