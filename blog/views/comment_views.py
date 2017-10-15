from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Comment
from blog.permissions import CommentPermission
from blog.serializers import CommentSerializer


class CommentListCreateAPIView(ListCreateAPIView):
    # Only authenticated users can comment a post. Everyone can create posts
    permission_classes = IsAuthenticatedOrReadOnly,

    # We want all comments of a post to be listed
    pagination_class = None

    serializer_class = CommentSerializer

    def get(self, request, post_pk):
        """
        List comments of a post
        """
        return self.list(request, post_pk)

    def post(self, request, post_pk):
        """
        Post a comment to post
        """
        return self.create(request, post_pk)

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Comment.objects.filter(
            post__is_published=True,
            post=post_pk,
            parent=None
        )

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post_pk")
        serializer.save(
            user=self.request.user,
            post=post_pk
        )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # We can use multiple permissions
    permission_classes = IsAuthenticatedOrReadOnly, CommentPermission,
    serializer_class = CommentSerializer

    def get(self, request, pk):
        """
        Retrieve comment with given id
        """
        return self.retrieve(request, pk)

    def put(self, request, pk):
        """
        Update comment with given id
        """
        return self.update(request, pk)

    def patch(self, request, pk):
        """
        Partially Update comment with given id
        """
        return self.partial_update(request, pk)

    def delete(self, request, pk):
        """
        Delete the comment with given id
        """
        return self.destroy(request, pk)

