from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Profile

User = get_user_model()

class UserRegistrationTestCase(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone": "1234567890",
            "password": "strongpassword",
            "password2": "strongpassword",
            "profile": {
                "fname": "Test",
                "lname": "User",
                "mname": "Middle",
                "address": "123 Test St",
                "pic": "default.jpg"
            }
        }

        self.invalid_payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone": "1234567890",
            "password": "strongpassword",
            "password2": "mismatchedpassword",
            "profile": {
                "fname": "Test",
                "lname": "User",
                "mname": "Middle",
                "address": "123 Test St",
                "pic": "default.jpg"
            }
        }

    def test_user_registration_success(self):
        """Test successful user registration."""
        response = self.client.post("/api/register/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User created Sucessfully")

        # Check if user and profile are created
        user = User.objects.get(username="testuser")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.fname, "Test")
        self.assertEqual(profile.lname, "User")

    def test_user_registration_password_mismatch(self):
        """Test user registration with mismatched passwords."""
        response = self.client.post("/api/register/", self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_error", response.data)
        self.assertEqual(response.data["non_field_error"], "Passwords did not match.")

    def test_user_registration_missing_profile(self):
        """Test user registration without profile data."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload.pop("profile")
        
        response = self.client.post("/api/register/", invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("profile", response.data)

    def test_user_registration_invalid_email(self):
        """Test user registration with invalid email."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "invalid-email"
        
        response = self.client.post("/api/register/", invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

