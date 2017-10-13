from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "username", "first_name", "last_name"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = "user", "created_at", "post"
        fields = "__all__"

    user = UserSerializer()


class PostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = "author", "liked_by", "created_at", "updated_at",
        fields = "__all__"

    comment_set = CommentSerializer(many=True)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = "author", "created_at", "updated_at",
        fields = "author", "created_at", "updated_at", "slug", "preview", "thumbnail", "tags"


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user =  username and password and authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        return {
            "user": user
        }
