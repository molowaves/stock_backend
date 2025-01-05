from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegisterTestCase(APITestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {'username':'user1', 'email':'user1@company.com',
                                               'phone':'+2348099563452', 'password':'secret', 
                                               'password2':'secret'}
        
        response =  self.client.post(url, data, format='json')
        expected_response = {'message':'User created Sucessfully'}

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_empty_user_name(self):
        url = reverse('register')
        data = {'username':'', 'email':'user1@company.com',
                                               'phone':'+2348099563452', 'password':'secret', 
                                               'password2':'secret'}
        
        response =  self.client.post(url, data, format='json')
        expected_response = {'username': ['This field may not be blank.']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


    def test_unique_user_name(self):
        url = reverse('register')
        data = {'username':'user1', 'email':'user1@company.com',
                                               'phone':'+2348099563452', 'password':'secret', 
                                               'password2':'secret'}
        
        data2 = {'username':'user1', 'email':'user2@company.com',
                                               'phone':'+2348099563451', 'password':'secret', 
                                               'password2':'secret'}
        
        response =  self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(url, data2, format='json')

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = {"username": ["A user with that username already exists."]}
        self.assertEqual(response2.data, expected_response)
        
    def test_empty_email(self):
            url = reverse('register')
            data = {'username':'user1', 'email':'',
                                                'phone':'+2348099563452', 'password':'secret', 
                                                'password2':'secret'}
            
            response =  self.client.post(url, data, format='json')
            expected_response = {'email': ['This field may not be blank.']}

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, expected_response)


    def test_unique_email(self):
        url = reverse('register')
        data = {'username':'user1', 'email':'user1@company.com',
                                                'phone':'+2348099563452', 'password':'secret', 
                                                'password2':'secret'}
            
        data2 = {'username':'user2', 'email':'user1@company.com',
                                                'phone':'+2348099563453', 'password':'secret', 
                                                'password2':'secret'}
            
        response =  self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(url, data2, format='json')

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = {"email": ["user with this email already exists."]}
        self.assertEqual(response2.data, expected_response)

    def test_password_mismatch(self):
        url = reverse('register')
        data = {'username':'user1', 'email':'user1@company.com',
                                                    'phone':'+2348099563452', 'password':'secret', 
                                                    'password2':'secre'}
        response = self.client.post(url, data, format='json')
        expected_response = {"non_field_error": "Passwords did not match."}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
                
