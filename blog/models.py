from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from celery.utils.text import truncate
from blog import managers
from blog.managers import PostManager


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = PostManager()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="written_post_set")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    preview = models.TextField()
    body = models.TextField()
    thumbnail = models.FileField()
    is_published = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_post_set")
    created_at = models.DateTimeField("Created Date", default=timezone.now)
    updated_at = models.DateTimeField("Update Date", default=timezone.now)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return truncate(self.title, maxlen=30)


class PublishedPost(Post):
    objects = managers.PublishedPostManager()

    class Meta:
        proxy = True
        verbose_name = _("Published Post")
        verbose_name_plural = _("Published Posts")


class Comment(models.Model):
    # Post has an author, Comment has a user. We will deal with this difference in views.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    parent = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="kids", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return truncate(self.body, maxlen=30)


# Signals
def update_timestamps(instance, **kwargs):
    instance.updated_at = timezone.now()


signals.pre_save.connect(update_timestamps, sender=Post)
signals.pre_save.connect(update_timestamps, sender=PublishedPost)


def set_slug(instance, **kwargs):
    if not instance.slug:
        instance.set_slug = slugify(instance.title)


signals.pre_save.connect(set_slug, sender=Post)
signals.pre_save.connect(set_slug, sender=PublishedPost)
