from rest_framework.test import APITestCase
from ..serializers import RegisterSerializer, ProfileSerializer, VerifyRegistrationSerializer
from ..models import OneTimePassword, User



class RegisterSerializerTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'username':'user1',
            'email':'email@company.com',
            'phone':'+2349166225544'
        }
    

    def test_register_serializer_save(self):
        serializer = RegisterSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(serializer.data, self.data)
        otp = OneTimePassword.objects.filter(id=1).first()
        self.assertIsNotNone(otp)




class ProfileSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='user1@gmail.com', password='secret')
        self.data = {
            'fname':'John',
            'lname':'Doe',
            'mname':'Smith',
            'address':'123 street',
        }


    def test_profile_serializer_save(self):
        serializer = ProfileSerializer(data=self.data)
        serializer.is_valid()
        serializer.save(user=self.user)
        self.assertEqual(serializer.data, self.data)


class VerifyRegistrationSerializerTestCase(APITestCase):
    def setUp(self):
        self.valid_data = {
            'username':'user1',
            'password':'secret',
            'password2':'secret',
            'OTP':'123'
        }

        self.invalid_data = {
            'username':'user1',
            'password':'secret',
            'password2':'sec',
            'OTP':'123'
        }

    def test_verify_create(self):
        serializer = VerifyRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())