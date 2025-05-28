from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AuthTests(APITestCase):

    def test_user_registration(self):
        url = reverse('register') 
        print(url)
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "test",
            "last_name": "test",
            "role": "patient",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_logout_with_refresh_token(self):
        user = User.objects.create_user(username="logoutuser", password="logoutpass")
        self.client.force_authenticate(user)
        refresh = str(RefreshToken.for_user(user))
        url = reverse('logout')  
        response = self.client.post(url, {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_with_invalid_token(self):
        user = User.objects.create_user(username="logoutuser2", password="logoutpass")
        self.client.force_authenticate(user)
        url = reverse('logout')
        response = self.client.post(url, {"refresh": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
