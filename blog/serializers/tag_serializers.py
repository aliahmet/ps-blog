from django.contrib.auth.models import User
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    model = User
    fields = "name"
