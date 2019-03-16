from rest_framework.test import APITestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

# Create your tests here.


class UserTests(APITestCase):

    def test_create_user(self):
        count = get_user_model().objects.count()
        print(count)
        response = self.client.post(reverse(
            'api:users-list'), {'username': 'apitester',
                                'password': 'api@1234'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(count+1, get_user_model().objects.count())

    def test_create_user_invalid_password(self):
        count = get_user_model().objects.count()
        self.client.post(reverse(
            'api:users-list'), {'username': 'apitester',
                                'password': '234'})
        self.assertNotEqual(count+1, get_user_model().objects.count())

    def test_create_user_invalid_mail(self):
        count = get_user_model().objects.count()
        self.client.post(reverse(
            'api:users-list'), {'username': 'apitester', 'email': 'apiappp.com',
                                'password': 'api@1234'})
        self.assertNotEqual(count+1, get_user_model().objects.count())

    def test_create_user_invalid_same(self):
        count = get_user_model().objects.count()
        response = self.client.post(reverse(
            'api:users-list'), {'username': 'apitester1',
                                'password': 'apitester1'})
        self.assertNotEqual(count+1, get_user_model().objects.count())
        self.assertEqual(response.status_code, 400)
