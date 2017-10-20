import json

from copy import deepcopy
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from blog.tests.helpers import CreateTestUserMixin


class AuthTest(CreateTestUserMixin, APITestCase):
    def setUp(self):
        self.register_url = 'register-api'
        self.login_url = 'login-api'
        self.user_retrieve_update_url = 'user-retrieve-update-api'

    def test_register_user_successful(self):
        """
        A Successful Registration
        Conditions:
        * Valid input data

        Checklist:
         1. Response is sucessfull
         2. User count is increaded by 1
         3. Last created user has the given password
         4. A token is returned
         5. Token is valid
         6. Token belongs to last created user
        """

        current_user_count = User.objects.count()

        data = {
            "username": "johndoe",
            "first_name": "john",
            "last_name": "doe",
            "password": "password is the most used password in 2017",
            "email": "johndoe@example.com"
        }
        response = self.client.post(reverse(self.register_url), data=data)

        # check 1
        self.assertEqual(201, response.status_code, response.content)

        # check 2
        new_user_count = User.objects.count()
        self.assertEqual(1, new_user_count - current_user_count, "There is less or more than 1 new user")

        # check 3
        newly_created_user = User.objects.order_by("pk").last()
        self.assertTrue(newly_created_user.check_password(data['password']))

        # check 4
        response_data = json.loads(response.content)
        self.assertIn("token", response_data.keys())

        # check 5 & 6
        self.assertTrue(Token.objects.filter(user=newly_created_user, key=response_data['token']).exists())

    def test_short_password_register(self):
        """
           Failed Registration because of short password

           Conditions:
           * Valid input data except password that is 3 char long

           Checklist:
            1. Response is unsucessfull
            2. User count is not changed
            3. Response has password error
           """

        current_user_count = User.objects.count()

        data = {
            "username": "johndoe",
            "first_name": "john",
            "last_name": "doe",
            "password": "abc",
            "email": "johndoe@example.com"
        }
        response = self.client.post(reverse(self.register_url), data=data)

        # check 1
        self.assertEqual(400, response.status_code, response.content)

        # check 2
        new_user_count = User.objects.count()
        self.assertEqual(0, new_user_count - current_user_count, "There is less or more than 0 new user")

        # check 3
        response_data = json.loads(response.content)
        self.assertIn("password", response_data.keys())

    def test_numeric_password_register(self):
        """
           Failed Registration because of fully numeric password

           Conditions:
           * Valid input data except password that is fully numeric

           Checklist:
            1. Response is unsucessfull
            2. User count is not changed
            3. Response has password error
           """

        current_user_count = User.objects.count()

        data = {
            "username": "johndoe",
            "first_name": "john",
            "last_name": "doe",
            "password": "123456789",
            "email": "johndoe@example.com"
        }
        response = self.client.post(reverse(self.register_url), data=data)

        # check 1
        self.assertEqual(400, response.status_code, response.content)

        # check 2
        new_user_count = User.objects.count()
        self.assertEqual(0, new_user_count - current_user_count, "There is less or more than 0 new user")

        # check 3
        response_data = json.loads(response.content)
        self.assertIn("password", response_data.keys())

    def test_common_password_register(self):
        """
           Failed Registration because of fully common password

           Conditions:
           * Valid input data except password that is commonly used

           Checklist:
            1. Response is unsucessfull
            2. User count is not changed
            3. Response has password error
           """

        current_user_count = User.objects.count()

        data = {
            "username": "johndoe",
            "first_name": "john",
            "last_name": "doe",
            "password": "password",
            "email": "johndoe@example.com"
        }
        response = self.client.post(reverse(self.register_url), data=data)

        # check 1
        self.assertEqual(400, response.status_code, response.content)

        # check 2
        new_user_count = User.objects.count()
        self.assertEqual(0, new_user_count - current_user_count, "There is less or more than 0 new user")

        # check 3
        response_data = json.loads(response.content)
        self.assertIn("password", response_data.keys())

    def test_register_existing_username_email(self):
        """
        Failed Registration because of existing username
        Failed Registration because of existing email

        Conditions:
        * 3 sets of data:
           #1: Valid input data
           #2: Valid, username same as 1
           #3: Valid, email same as 2

        Checklist:
         1. Register of #1 is sucessful
         2. Register of #2 is unsuccessful
         3. Register of #2 has key username
         4. Register of #3 is successful
                    # (Django doesn't require unique email by default)
         5. Register of #3 has key token
        """

        def register_helper(data):
            """
            Register helper function
            """
            response = self.client.post(reverse(self.register_url), data=data)
            return response.status_code, json.loads(response.content)

        data1 = {
            "username": "johndoe",
            "first_name": "john",
            "last_name": "doe",
            "password": "password is the most used password in 2017",
            "email": "johndoe@example.com"
        }
        data2 = {
            "username": "johndoe",
            "first_name": "johnathan",
            "last_name": "doe",
            "password": "password is the most used password in 2017",
            "email": "johnathandoe@example.com"
        }
        data3 = {
            "username": "johnathandoe",
            "first_name": "johnathan",
            "last_name": "doe",
            "password": "password is the most used password in 2017",
            "email": "johndoe@example.com"
        }

        # Check 1
        status_1, response_data1 = register_helper(data1)
        self.assertEqual(201, status_1, response_data1)

        # Check 2
        status_2, response_data2 = register_helper(data2)
        self.assertEqual(400, status_2, response_data2)

        # Check 3
        self.assertIn("username", response_data2.keys())

        # Check 4
        status_3, response_data3 = register_helper(data3)
        self.assertEqual(201, status_3, response_data3)

        # Check 5
        self.assertIn("token", response_data3.keys())

    def test_missing_and_extra_data(self):
        """
        Registration with missing and extra data
        Conditions:
        * All existing data, if actually required, is valid

        Checklist:
         1. Missing Password: Fail
         2. Empty Password: Fail

         3. Missing Username: Fail
         4. Empty UserName: Fail

         5. Missing First Name: Success
         6. Empty First Name: Success

         7. Missing Last Name: Success
         8. Empty Last Name: Success

         9. Missing Email: Success
         10. Empty Email: Success

         11. Extra gender: Success # should be ignored
        """

        valid_data = {
            "username": "johndoe",
            "first_name": "john",
            "last_name": "doe",
            "password": "password is the most used password in 2017",
            "email": "johndoe@example.com"
        }

        def register_helper(data):
            """
            Register helper function
            """
            response = self.client.post(reverse(self.register_url), data=data)
            return response.status_code, json.loads(response.content)

        # Check 1
        data = deepcopy(valid_data)
        data.pop("password")
        status, response_data = register_helper(data)
        self.assertEqual(400, status, response_data)
        User.objects.all().delete()

        # Check 2
        data = deepcopy(valid_data)
        data["password"] = ""
        status, response_data = register_helper(data)
        self.assertEqual(400, status, response_data)
        User.objects.all().delete()

        # Check 3
        data = deepcopy(valid_data)
        data.pop("username")
        status, response_data = register_helper(data)
        self.assertEqual(400, status, response_data)
        User.objects.all().delete()

        # Check 4
        data = deepcopy(valid_data)
        data["username"] = ""
        status, response_data = register_helper(data)
        self.assertEqual(400, status, response_data)
        User.objects.all().delete()

        # Check 5
        data = deepcopy(valid_data)
        data.pop("first_name")
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
        User.objects.all().delete()

        # Check 6
        data = deepcopy(valid_data)
        data["first_name"] = ""
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
        User.objects.all().delete()

        # Check 7
        data = deepcopy(valid_data)
        data.pop("last_name")
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
        User.objects.all().delete()

        # Check 8
        data = deepcopy(valid_data)
        data["last_name"] = ""
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
        User.objects.all().delete()

        # Check 9
        data = deepcopy(valid_data)
        data.pop("email")
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
        User.objects.all().delete()

        # Check 10
        data = deepcopy(valid_data)
        data["email"] = ""
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
        User.objects.all().delete()

        # Check 11
        data = deepcopy(valid_data)
        data["gender"] = "male"
        status, response_data = register_helper(data)
        self.assertEqual(201, status, response_data)
