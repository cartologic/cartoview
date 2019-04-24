import pytest
from django.shortcuts import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

fake = Faker()


@pytest.mark.django_db
@pytest.mark.usefixtures("test_initial_users")
class UserCreateTests(APITestCase):
    def get_valid_user_data(self):
        return {'username': fake.user_name(),
                'email': fake.email(),
                'password': fake.password()}

    def get_invalid_user_data(self):
        return {'username': fake.user_name(),
                'email': fake.address(),
                'password': fake.numerify()}

    def test_create_user(self):
        response = self.client.post(reverse(
            'api:users-list'), self.get_valid_user_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        resp = self.client.post(reverse(
            'api:users-list'), self.get_invalid_user_data())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
