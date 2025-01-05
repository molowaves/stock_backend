from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserRegisterSerializer

@api_view(['POST'])
def index(request):
    print('FILE', request.FILES)
    print('DATA', request.data['data'])

    return Response({'data':'Data'})

@api_view(['POST'])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'User created Sucessfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

