from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.db.models import Q
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User, OneTimePassword, Store
from .serializers import (RegisterSerializer, ProfileSerializer, 
                          VerifyRegistrationSerializer, StoreSerializer
                          )
from .utils import send_reg_otp

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def register(request):
    '''
    This function registers a new employee account and profile
    altogether and sends an email with a one time password along
    with an instruction to change the password. The OTP is saved in
    base64 encoded format.
    '''

    user_serializer = RegisterSerializer(data=request.data) 
    profile_serializer = ProfileSerializer(data=request.data)


    if user_serializer.is_valid() and profile_serializer.is_valid():
        user_serializer.save()
        user = User.objects.get(username=user_serializer.data['username'])
        profile_serializer.save(user=user)

        OTP = OneTimePassword.objects.get(user=user)
        send_reg_otp(user=user, OTP=urlsafe_base64_decode(str(OTP)))
    
        return Response({'message':'An email has been sent to the address you provided with an instruction to reset your password.'})
    
    # Checks for errors
    errs = {}
    if user_serializer.errors:
        errs = user_serializer.errors
    elif profile_serializer.errors:
        errs = profile_serializer.errors

    return Response(errs, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
def verify_registration(request):
        '''
        This function verifies the employee's email address
        using the OTP sent to the employee's email address
        '''

        serializer = VerifyRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'] #Retrieves validated user name
            try:
                user = User.objects.get(Q(email=username) | Q(username=username) | Q(phone=username)) #gets user by either username, email or phone number
                submitted_otp = urlsafe_base64_encode(str(serializer.validated_data['OTP']).encode('utf-8')) #Gets the submitted otp

                otp_user= OneTimePassword.objects.filter(user=user, OTP=submitted_otp) #Retrieves the actual otp
                if otp_user.count() > 0:
                    serializer.save()
                    otp_user[0].delete()
                    return Response({'message':'Account successfully verified. You can now login using your new credentials.'})
                return Response({'non_field_error':'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'non_field_error':'User does not exists'})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]