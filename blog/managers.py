from django.db.models import QuerySet, Count, F
from django.db.models.manager import BaseManager


class PostQuerySet(QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PostManager(BaseManager.from_queryset(PostQuerySet)):
    def get_queryset(self):
        return super().get_queryset().annotate(
            comment_count=Count("comment", distinct=True),
            like_count=Count("liked_by", distinct=True),
            points=F("comment_count") + F("like_count")
        )


class PublishedPostManager(PostManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.published()
