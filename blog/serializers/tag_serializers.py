from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "name",
