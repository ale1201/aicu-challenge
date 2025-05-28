from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDetailView


urlpatterns = [
    path('', UserDetailView.as_view(), name='user_detail'),
]