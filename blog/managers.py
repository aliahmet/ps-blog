from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class PostQuerySet(QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PostManager(BaseManager.from_queryset(PostQuerySet)):
    pass


class PublishedPostManager(PostManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.published()
