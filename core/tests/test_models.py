from django.test import TestCase
from ..models import User, Profile, OneTimePassword, Store


class UserModelTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user1', email='user1@company.com', 
                                 password='secret', phone='09022334455')

    def test_object_name_is_username(self):
        user = User.objects.get(pk=1)
        expected_object_name =  str(user.username)
        self.assertEqual(str(user), expected_object_name)


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='user1@company.com', 
                                 password='secret', phone='09022334455')
        
        self.profile = Profile.objects.create(fname='John', lname ='Doe', 
                                              mname='Smith', address='123 street',
                                              user=self.user
                                              )

    def test_object_name_is_fname_lname_mname(self):
        profile = Profile.objects.get(pk=1)
        expected_object_name =  f'{self.profile.fname} {self.profile.lname} {self.profile.mname}'
        self.assertEqual(str(profile), expected_object_name)


class StoreModelTestCase(TestCase):
    def setUp(self):
        Store.objects.create(name='Maraba', location='Kaduna')

    def test_object_name_is_profile_name(self):
        profile = Store.objects.get(pk=1)
        expected_object_name =  profile.name
        self.assertEqual(str(profile), expected_object_name)



class OneTimePasswordModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='user1@company.com', 
                                 password='secret', phone='09022334455')
        
        self.otp = OneTimePassword.objects.create(user=self.user)

    def test_object_name_is_fname_lname_mname(self):
        OTP = OneTimePassword.objects.get(pk=1)
        expected_object_name =  str(self.otp.OTP)
        self.assertEqual(str(OTP), expected_object_name)

         


