from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS


def IsOwnerOrReadOnly(owner_field):
    """
    I prefer to name class generator functions in CamelCase.
    (PEP8 tells us to name them in snake_case)
    """

    class _IsOwnerOrReadOnly(BasePermission):
        def has_object_permission(self, request, view, obj):
            return (
                request.method in SAFE_METHODS or
                request.user and
                is_authenticated(request.user) and
                getattr(obj, owner_field) == request.user
            )

    return _IsOwnerOrReadOnly


class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            request.user and
            is_authenticated(request.user) and
            obj == request.user
        )


class CommentPermission(BasePermission):
    """
    A comment can be deleted or changed by its user
    A comment can be deleted by the user of the post
    """

    def has_object_permission(self, request, view, obj):
        # Clarify what is what
        user = request.user
        comment = obj
        post = obj.post

        if request.method in SAFE_METHODS:
            return True
        # At this point we know request is either POST, PUT, PATCH or DELETE

        if not user or not is_authenticated(user):
            return False
        # Now we also know user is authenticated

        if request.method == "POST":
            return True
        # At this point we know request is either PUT, PATCH or DELETE

        if request.method == "DELETE":
            return request.user in (comment.user, post.author)
        # At this point we know request is either PUT or PATCH

        return request.user == comment.user
