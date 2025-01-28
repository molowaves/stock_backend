from rest_framework import serializers
from django.db.models import Q
from .models import User, Profile, OneTimePassword


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']


    def save(self):
        user = User(username=self.validated_data['username'],
                    email = self.validated_data['email'],
                    phone = self.validated_data['phone'],
                    )
        user.save()
        OneTimePassword.objects.create(user=user)
        return user
    


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']

    def save(self, *args, **kwargs):
        profile = Profile(fname=self.validated_data.get('fname'), lname=self.validated_data.get('lname'),
                          mname=self.validated_data.get('mname'), address=self.validated_data.get('address'),
                          pic=self.validated_data.get('pic'), user=kwargs['user'])
        profile.save()
        return profile
    




class VerifyRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, style={'input_type':"password"}, write_only=True)
    password2 = serializers.CharField(max_length=100, style={'input_type':"password"}, write_only=True)
    OTP = serializers.IntegerField(min_value=000000, max_value=999999)


    def create(self, validated_data):
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password != password2:
            raise serializers.ValidationError({'non_field_error':'Password mismatch.'})
        
        username = validated_data.get('username')
        user = User.objects.get(Q(email=username) | Q(username=username) | Q(phone=username))
        user.reg_status = 'R'
        user.set_password(password)
        user.save()

        return user
    

       
    
    