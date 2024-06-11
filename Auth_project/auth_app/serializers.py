from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
