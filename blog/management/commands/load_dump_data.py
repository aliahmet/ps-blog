from math import sqrt, pi, exp
from random import randint, choice, sample, random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.lorem_ipsum import paragraph, sentence, paragraphs, words, WORDS

from blog.models import Post, Tag, Comment

NUMBER_OF_USERS = 10
NUMBER_OF_POSTS = 100

COMMENT_COUNT_MAX = 10


def comment_count():
    return randint(0, COMMENT_COUNT_MAX)


class Command(BaseCommand):
    def handle(self, **options):
        if not User.objects.exists():
            usernames = words(NUMBER_OF_USERS).split(" ")
            User.objects.bulk_create([
                User(username=username, password=username, email="%s@gmail.com" % username)
                for username in usernames
            ])

        if not Tag.objects.exists():
            Tag.objects.bulk_create([Tag(name=word) for word in WORDS])

        if not Post.objects.exists():
            users = list(User.objects.all())
            tags = list(Tag.objects.all())
            for p in range(NUMBER_OF_POSTS):
                post = Post.objects.create(
                    author=choice(users),
                    title=sentence(),
                    body="\n".join(paragraphs(randint(3, 5))),
                    thumbnail="http://test.com/test.jpg",
                    is_published=choice([True, True, False]),

                )
                post.tags.add(*sample(tags, randint(0, 10)))
                post.liked_by.add(*sample(users, randint(0, 10)))

                for i in range(comment_count()):
                    Comment.objects.create(
                        user=choice(users),
                        body=paragraph(),
                        post=post,
                        parent= None if random() < 0.5 or not post.is_published else choice(post.comment_set.all() or [None])                    )
