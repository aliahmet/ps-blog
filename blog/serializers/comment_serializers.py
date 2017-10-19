from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from blog.models import Comment
from blog.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = "id", "user", "created_at", "post", "kids"
        fields = "id", "user", "created_at", "post", "kids", "body",

    user = UserSerializer()
    kids = RecursiveField(many=True)
