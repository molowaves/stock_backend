import random
from django.db import models
from django.contrib.auth.models import AbstractUser

REG_STATUS = [
    ('R', 'registered'),
    ('P', 'pending')
]

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    reg_status = models.CharField(max_length=2, choices=REG_STATUS)
    
    def __str__(self):
        return self.username
    

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    OTP = models.CharField(max_length=50, default=random.randrange(100000, 999999), blank=True)

    def __str__(self):
        return self.OTP

class Profile(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    pic = models.ImageField(upload_to='emp/passports', default='default.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.mname:
            return f"{self.fname} {self.lname} {self.mname}"
        return f"{self.fname} {self.lname}"


