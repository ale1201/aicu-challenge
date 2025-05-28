from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from .serializers import UserSerializer


class UserDetailView(APIView):
    """
    API view for authenticated users to manage their profile.

    Supported actions:
    - GET: Retrieve user details.
    - PUT: Update user information (partial update).
    - DELETE: Delete user and optionally blacklist refresh token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieve details of the currently authenticated user.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """
        Partially update the authenticated user's information.

        Returns:
            200 OK on success,
            400 Bad Request if data is invalid.
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Deletes the authenticated user and invalidates the refresh token if provided.

        Returns:
            204 No Content on success.
        """
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                raise ValidationError("Invalid refresh token.")

        request.user.delete()
        return Response({"detail": "User deleted and logged out."}, status=status.HTTP_204_NO_CONTENT)
