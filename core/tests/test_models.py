from django.test import TestCase
from ..models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user1', email='user1@company.com', 
                                 password='secret', phone='09022334455')

    def test_object_name_is_username(self):
        user = User.objects.get(pk=1)
        expected_object_name =  str(user.username)
        self.assertEqual(str(user), expected_object_name)

         


