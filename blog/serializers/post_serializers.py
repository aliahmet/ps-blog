from rest_framework import serializers

from blog.models import Post
from blog.serializers import CommentSerializer, TagSerializer, UserSerializer


class PostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = "author", "liked_by", "created_at", "updated_at",
        fields = "__all__"

    comment_set = CommentSerializer(many=True)


class PostPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = "author", "created_at", "updated_at", "like_count", "comment_count"
        fields = "author", "like_count", "comment_count", "created_at", "updated_at", "slug", "preview", "thumbnail", "tags"

    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()

    tags = TagSerializer(many=True)
    author = UserSerializer()
