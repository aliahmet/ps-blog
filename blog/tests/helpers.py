import random
import string

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def random_token_generator(len=32, lower=True, upper=False, numbers=False, punctuation=False, extra=""):
    chars = ""
    if lower:
        chars += string.ascii_lowercase

    if upper:
        chars += string.ascii_uppercase

    if numbers:
        chars += string.digits

    if punctuation:
        chars += punctuation

    chars += extra

    return "".join([random.choice(chars) for i in range(len)])


class CreateTestUserMixin:
    """
    Creates test users.
    usage: self.create_user(username="xxx" ... )
           or
           self.create_user() # Fully random

    """
    def create_superuser(self, **kwargs):
        kwargs.setdefault("is_superuser", True)
        return self.create_user(**kwargs)

    def create_user(self, **kwargs):
        random_string = random_token_generator(len=12, lower=True)
        kwargs.setdefault("username", random_string)
        kwargs.setdefault("email", "%s@test.com" % random_string)
        kwargs.setdefault("password", random_string)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        generate_token =  kwargs.pop("generate_token", False)
        user = User.objects._create_user(**kwargs)
        if generate_token:
            Token.objects.get_or_create(user=user)
        return user

