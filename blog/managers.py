from django.db import models


class PostManager(models.Manager):
    def published(self):
        return self.filter(is_published=True)


class PublishedPostManager(PostManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.published()
