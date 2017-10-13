from django.core.management import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    def handle(self, **options):
        Post.objects.update(is_published=True)
        print("All posts are now published!")
