from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','role','phone_number','avatar')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "role", "phone_number")
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
    
