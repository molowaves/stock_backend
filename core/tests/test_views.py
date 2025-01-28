import io, secrets, os
from PIL import Image

from rest_framework import status, permissions
from rest_framework.test import APITestCase, force_authenticate
from django.urls import reverse
from unittest.mock import Mock, patch
from django.utils.http import urlsafe_base64_decode
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from ..serializers import RegisterSerializer, StoreSerializer
from ..models import User, OneTimePassword, Profile, Store


class RegistrationTestCase(APITestCase):
    def generate_test_image(self):
        image = Image.new('RGB', (100, 100), color='blue')
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        return byte_arr
       

    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='superuser@gmail.com', 
                                                  password='secret', username='username')
        
        self.client.force_login(user=self.admin_user)
        image = self.generate_test_image()
 
        self.simpleuploadedfile = SimpleUploadedFile(
            name= str(secrets.token_urlsafe()) + '.jpg',
            content=image.read(),
            content_type='image/jpeg'
        )

        self.data = {
            'username':'user1',
            'email':'user1@company.com',
            'fname':'John',
            'lname':'Doe',
            'mname':'Smith',
            'address':'123 street',
            'phone':'+2349867543345',
            'pic':self.simpleuploadedfile
        }

        self.invalid_data = {
            'username':'user1',
            'email':'usercompany.com',
            'fname':'John',
            'lname':'Doe',
            'mname':'Smith',
            'address':'123 street',
            'phone':'+2349867543345',
        }

       
    @patch('core.views.send_reg_otp')
    def test_register_success(self, mock_send_reg_otp):
        url = reverse('register')
        mock_send_reg_otp.return_value.status_code = None

        
        response = self.client.post(url, self.data)
        expected_response =  {'message':'An email has been sent to the address you provided with an instruction to reset your password.'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())


         # Assert send_reg_otp was called once with the expected arguments
        user = User.objects.get(username=self.data['username'])
        otp = OneTimePassword.objects.get(user=user)
        mock_send_reg_otp.assert_called_once_with(user=user, OTP=urlsafe_base64_decode(otp.OTP))


    @patch('core.views.send_reg_otp')
    def test_register_failure(self, mock_send_reg_otp):
        """Test registration failure with invalid data"""
        url = reverse('register')
        response = self.client.post(url, self.invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        mock_send_reg_otp.assert_not_called()


class RegistrationVerificationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='user1@company.com', 
                                        phone='+2349177665544')
        self.otp = OneTimePassword.objects.create(user=self.user)
        self.profile = Profile.objects.create(fname='John', lname='Doe', mname='Smith', 
                                              address='123 street', user=self.user)
        self.valid_data = {
            'username':self.user.username,
            'password':'secret',
            'password2':'secret',
            'OTP':urlsafe_base64_decode(self.otp.OTP).decode('utf-8')
        }


        self.invalid_data = {
            'username':self.user.username,
            'password':'secret',
            'password2':'secret',
            'OTP':3422
        }


        self.passwords_mismatch = {
            'username':self.user.username,
            'password':'secret',
            'password2':'sec',
            'OTP':urlsafe_base64_decode(self.otp.OTP).decode('utf-8')
        }

    def test_verify_reg_success(self):
        url = reverse('verify_reg')
        response = self.client.put(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_reg_invalid_otp(self):
        url = reverse('verify_reg')
        response = self.client.put(url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({'non_field_error': 'Invalid OTP'}, response.data)


    def test_password_mismatch(self):
        url = reverse('verify_reg')
        response = self.client.put(url, self.passwords_mismatch)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({'non_field_error': 'Password mismatch.'}, response.data)
    


class StoreTestCase(APITestCase):
    def setUp(self):
        self.store = Store.objects.create(name='Maraba', location='By AP filling station')
        self.admin_user = User.objects.create_superuser(email='superuser@gmail.com', 
                                                  password='secret', username='username')
        
        self.non_admin_user = User.objects.create_user(email='normal@gmail.com', password='secret', 
                                username='normalusername', phone='+2349122334455')

        self.data = {
            'name':'First store',
            'location':'Kujama'
        }



    def test_list_stores_admin_user(self):
        self.client.force_login(user=self.admin_user)
        url = reverse('store-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer =  StoreSerializer([self.store], many=True)
        self.assertEqual(response.data, serializer.data)



    def test_retrieve_store(self):
        self.client.force_login(user=self.non_admin_user)
        url =  reverse('store-detail', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = StoreSerializer(self.store)
        self.assertEqual(response.data, serializer.data)

    def test_create_store_success(self):
        self.client.force_login(user=self.admin_user)
        url =  reverse('store-list')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_output = {'id':2, **self.data}
        self.assertEqual(response.data, expected_output)
    

    def test_create_store_failure(self):
        self.client.force_login(user=self.non_admin_user)
        url =  reverse('store-list')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_store_success(self):
        self.client.force_login(user=self.admin_user)
        url =  reverse('store-detail', kwargs={'pk':1})
        data = {'id':1, **self.data}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


    def test_update_store_failure(self):
        self.client.force_login(user=self.non_admin_user)
        url =  reverse('store-detail', kwargs={'pk':1})
        data = {'id':1, **self.data}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_store_success(self):
        self.client.force_login(user=self.admin_user)
        url =  reverse('store-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_update_store_failure(self):
        self.client.force_login(user=self.non_admin_user)
        url =  reverse('store-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)