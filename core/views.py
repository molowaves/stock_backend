from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import UserRegisterSerializer
from .models import User
from .utils import send_reg_otp



class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            send_reg_otp(email=serializer.data['email'], username=serializer.data['username'], OTP=serializer.data['OTP'])       
            return Response({'message':'User created Sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)