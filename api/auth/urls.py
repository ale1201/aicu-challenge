from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User registration
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('logout/', LogoutView.as_view(), name='logout'),
]
