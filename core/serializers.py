from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User(username=self.validated_data['username'],
                    email = self.validated_data['email'],
                    phone =  self.validated_data['phone']
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'non_field_error':'Passwords did not match.'})
        user.set_password(password)
        user.save()
        return user