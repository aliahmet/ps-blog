from django.conf.urls import url, include
from rest_framework.authtoken.views import ObtainAuthToken

from blog.views.auth_views import AuthTokenAPIView
from blog.views.comment_views import CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView
from blog.views.post_views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView
from blog.views.post_views import PostUnlikeAPIView, PostLikeAPIView
from blog.views.swagger import SwaggerSchemaView

urlpatterns = [
    url(r'^api-explorer/', SwaggerSchemaView.as_view(), name="api-explorer"),

    url(r'^api/v1.0/login/', AuthTokenAPIView.as_view()),

    url(r'^api/v1.0/post/', PostListCreateAPIView.as_view(), name="post-list-create-api"),
    url(r'^api/v1.0/post/(?P<pk>[0-9]+)/', PostRetrieveUpdateDestroyAPIView.as_view(),
        name="post-retrieve-destroy-update-api"),
    url(r'^api/v1.0/post/(?P<pk>[0-9]+)/like/', PostUnlikeAPIView.as_view(),
        name="post-like-api"),
    url(r'^api/v1.0/post/(?P<pk>[0-9]+)/unlike/', PostLikeAPIView.as_view(),
        name="post-unlike-api"),
    url(r'^api/v1.0/post/(?P<post_pk>[0-9]+)/comments/', CommentListCreateAPIView.as_view(),
        name="comment-list-create-api"),
    url(r'^api/v1.0/comment/(?P<pk>[0-9]+)/', CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-list-create-api"),

    # Use versioning even if it is very simple
    # We can now encourage using new endpoint while we support the
    #    old one for a limited time
    # Most Preferred:  Semantic (X.Y.Z) or Loose Semantic (X.Y)
    # See Also: NamespaceVersioning
    # url(r'^api/v1.1/post/', PostListCreateAPIViewWithADifferrentSerializer.as_view(), name="post-list-create-api"),

]
