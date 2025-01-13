import os, io
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile



class UserRegisterTestCase(APITestCase):
    def setUp(self):
        buffer = io.BytesIO()

        # Use PIL to generate an image (e.g., a red square)
        image = Image.new('RGB', (100, 100), color='red')
        image.save(buffer, format='PNG')
        buffer.seek(0)  # Reset buffer pointer to the beginning

        # Step 2: Create the InMemoryUploadedFile
        self.uploaded_file = InMemoryUploadedFile(
            file=buffer,  # The file-like object
            field_name='image',  # The field name where the file will be uploaded
            name='test_image.png',  # The name of the file
            content_type='image/png',  # The MIME type
            size=buffer.tell(),  # The file size
            charset=None,  # Encoding (optional, usually None for binary files)
        )

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username':'user1', 'email':'user1@company.com',
                                                    'phone':'+2348099563452', 'password':'secret', 'password2':'secret',
                                                    'fname':'Iliya','lname':'Peter','mname':'Maimolo','address':'123 Street',
                                                    'pic':self.uploaded_file
                                                    }
                                                    
        
        response =  self.client.post(url, data, format='multipart')
        expected_response = {'message':'User created Sucessfully'}

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)