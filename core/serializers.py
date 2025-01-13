from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class UserRegisterSerializer(serializers.Serializer):
    fname = serializers.CharField(max_length=100)
    lname = serializers.CharField(max_length=100)
    mname = serializers.CharField(max_length=100, allow_blank=True)
    address = serializers.CharField(max_length=500)
    pic = serializers.ImageField()
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = User(username=self.validated_data['username'],
                    email = self.validated_data['email'],
                    phone =  self.validated_data['phone']
                    )
            
        saved_user = user.save()

        fname = self.validated_data.get('fname')
        lname = self.validated_data.get('lname')
        mname = self.validated_data.get('mname')
        address = self.validated_data.get('address')
        pic = self.validated_data.get('pic')

        Profile.objects.create(user=user, fname=fname, lname=lname, 
                               mname=mname, address=address, pic=pic
                               )
        return user
    
    def to_representation(self, instance):
        output = {
            'username':instance.username,
            'email':instance.email,
            'fname':instance.profile.fname,
            'lname':instance.profile.lname,
        }
        return output