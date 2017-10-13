from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.metadata import BlogMetadata
from blog.models import Post
from blog.pagination import PostCursorPagination
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import PostSerializer, PostDetailsSerializer


class PostListCreateAPIView(ListCreateAPIView):
    """
    Model operations on Post: list, create
    Model = no pk
    """

    # Only authenticated users can create posts. Everyone can create posts
    permission_classes = IsAuthenticatedOrReadOnly,

    # Posts should be paginated
    pagination_class = PostCursorPagination

    # Posts can be searched or filtered by users
    filter_backends = DjangoFilterBackend, SearchFilter
    search_fields = "body",
    filter_fields = "author",

    serializer_class = PostSerializer
    metadata_class = BlogMetadata

    sample_response = {
        "message": "ok"
    }

    def get(self, request):
        """
        List posts
        """
        return self.list(request)

    def post(self, request):
        """
        Create new post
        """
        return self.create(request)

    def get_queryset(self):
        # Only published posts should be returned
        return Post.objects.published()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Single object operations on Post: retrieve, update, destroy
    Single object = pk
    """

    # Everyone can retrieve a post but only owner can alter it
    permission_classes = IsOwnerOrReadOnly(owner_field="author"),

    serializer_class = PostDetailsSerializer

    def get_object(self):
        """
        Only author can retrieve un published post
        """
        pk = self.kwargs.get("pk")
        query = Q(is_published=True)
        if self.request.user.is_authenticated():
            query = query | Q(author=self.request.user)
        query = Q(pk=pk) & query
        # WHERE id=99 AND (is_published=1 or author=12) <- if authenticated
        # or
        # WHERE id=99 AND is_published=1                <- if not authenticated
        return get_object_or_404(Post, query)

    def get(self, request, pk):
        """
        Retrieve a Post
        """
        return self.retrieve(request, pk)

    def put(self, request, pk):
        """
        Update a Post
        """
        return self.update(request, pk)

    def patch(self, request, pk):
        """
        Partially update a Post
        """
        return self.partial_update(request, pk)

    def delete(self, request, pk):
        """
        Delete a post and its comments
        """
        return self.destroy(request, pk)


class PostLikeUnlikeBaseAPIView(APIView):
    """
    Base class to handle like/unlike
    """
    permission_classes = IsAuthenticated,

    serializer_class = PostSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Post.objects.published(), pk=pk)

    def post_liked(self):
        post = self.get_object()
        return post.liked_by.filter(pk=self.request.user.pk).exists()


class PostLikeAPIView(PostLikeUnlikeBaseAPIView):
    def post(self, request, pk):
        """
        Like a Post
        """
        post = self.get_object()
        if self.post_liked():
            raise PermissionDenied("Post already liked!")
        post.liked_by.add(request.user)
        return Response({"message": "Post liked"})


class PostUnlikeAPIView(PostLikeUnlikeBaseAPIView):
    def post(self, request, pk):
        """
        Unlike a Post
        """
        post = self.get_object()
        if not self.post_liked():
            raise PermissionDenied("Post not liked!")
        post.liked_by.remvove(request.user)
        return Response({"message": "Post unkliked"})
