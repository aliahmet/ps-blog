from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^schema/$', views.SwaggerSchemaView.as_view(), name="api-explorer"),

    url(r'^api/v1.0/auth/login/$', views.LoginAPIView.as_view()),
    url(r'^api/v1.0/auth/register/$', views.RegisterAPIView.as_view()),
    url(r'^api/v1.0/auth/user/(?P<pk>[0-9]+)/$', views.UserRetrieveUpdateAPIView.as_view()),

    url(r'^api/v1.0/post/$', views.PostListCreateAPIView.as_view(), name="post-list-create-api"),
    url(r'^api/v1.0/post/(?P<pk>[0-9]+)/$', views.PostRetrieveUpdateDestroyAPIView.as_view(),
        name="post-retrieve-destroy-update-api"),
    url(r'^api/v1.0/post/(?P<pk>[0-9]+)/like/$', views.PostUnlikeAPIView.as_view(),
        name="post-like-api"),
    url(r'^api/v1.0/post/(?P<pk>[0-9]+)/unlike/$', views.PostLikeAPIView.as_view(),
        name="post-unlike-api"),
    url(r'^api/v1.0/post/(?P<post_pk>[0-9]+)/comments/$', views.CommentListCreateAPIView.as_view(),
        name="comment-list-create-api"),
    url(r'^api/v1.0/comment/(?P<pk>[0-9]+)/$', views.CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-list-create-api"),

    # Use versioning even if it is very simple
    # In case we need to change an end point, we can now encourage using new endpoint while
    #    supporting the old one for a limited time
    # Most Preferred:  Semantic (X.Y.Z) or Loose Semantic (X.Y)
    # See Also: NamespaceVersioning
    # ex: url(r'^api/v1.1/post/', PostListCreateAPIViewWithADifferrentSerializer.as_view(), name="post-list-create-api"),

]
