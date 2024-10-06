from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']

class UserRegistrationserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'password', 'username']
        extra_kwards = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        created_user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            username = validated_data['username'],
        )

        return created_user

class Userloginserializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()