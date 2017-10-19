from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "username", "first_name", "last_name", "email", "password"

    def validate(self, attrs):
        password = attrs.get("password")
        if password:
            attrs["password"] = make_password(password)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "id", "username", "first_name", "last_name", "email"
        read_only_fields = "id", "email"


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = username and password and authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        return {
            "user": user
        }
