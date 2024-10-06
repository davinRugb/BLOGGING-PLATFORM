from rest_framework import generics,permissions,status
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationserializer,UserSerializers, Userloginserializers
from rest_framework.authtoken.models import Token              
from rest_framework.authtoken.views import ObtainAuthToken


User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationserializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # if user.objects.filter(email=request.data['email']).exists():
        #     return Response({
        #     "message":"This Email Already Exists",
        # },status=status.HTTP_400_CREATED)

        # if user.objects.filter(username=request.data['username']).exists():
        #     return Response({
        #     "message":"This Email Already Exists",
        # },status=status.HTTP_400_CREATED)

        serializer.is_valid(raise_exception=True)  # Validate data
        user = serializer.save()  # Create the user
        user_data = UserRegistrationserializer(user).data
        return Response({
            "message":"User created successfully",
            "user":user_data,
        },status=status.HTTP_201_CREATED)

class ListAllUsers(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializers

class Userlogin(ObtainAuthToken):
    serializer_class = Userloginserializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate data
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "message": 'Invalid Email or Password',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check password
        if user.check_password(password):
            # Create tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": 'User Login successful',
                'user': UserSerializers(user).data,
                "accessToken": str(refresh.access_token),
                "refreshToken": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": 'Invalid Email or Password',
            }, status=status.HTTP_400_BAD_REQUEST)


