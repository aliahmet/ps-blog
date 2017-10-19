from blog.views.auth_views import LoginAPIView, RegisterAPIView, UserRetrieveUpdateAPIView
from blog.views.comment_views import CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView
from blog.views.post_views import PostRetrieveUpdateDestroyAPIView, PostLikeUnlikeBaseAPIView, PostLikeAPIView, \
    PostListCreateAPIView, PostUnlikeAPIView
from blog.views.swagger import SwaggerSchemaView

__ALL__ = [
    "LoginAPIView", "RegisterAPIView", "UserRetrieveUpdateAPIView",
    "CommentListCreateAPIView", "CommentRetrieveUpdateDestroyAPIView",
    "PostRetrieveUpdateDestroyAPIView", "PostLikeUnlikeBaseAPIView", "PostLikeAPIView", "PostListCreateAPIView",
    "PostListCreateAPIView", "PostUnlikeAPIView",
    "SwaggerSchemaView"

]
