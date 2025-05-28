from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthRecordViewSet

router = DefaultRouter()
router.register('', HealthRecordViewSet, basename='healthrecords')

urlpatterns = [
    path('', include(router.urls)),
]