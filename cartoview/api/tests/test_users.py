from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework.test import APITestCase

# Create your tests here.


class UserCreateTests(APITestCase):
    fixtures = ['users_data']

    def test_create_user(self):
        count = get_user_model().objects.count()
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
            'api:users-list'), {'username': 'apitester',
                                'email': 'apiappp.com',
                                'password': 'api@1234'})
        self.assertNotEqual(count+1, get_user_model().objects.count())

    def test_create_user_invalid_same(self):
        count = get_user_model().objects.count()
        response = self.client.post(reverse(
            'api:users-list'), {'username': 'apitester1',
                                'password': 'apitester1'}, format='json')
        self.assertNotEqual(count+1, get_user_model().objects.count())
        self.assertEqual(response.status_code, 400)


class UserUpdateTests(APITestCase):
    fixtures = ['users_data']

    def get_update_url(self):
        url = reverse('api:users-detail', kwargs={'pk': 4})
        return url

    def get_updated_user(self):
        return get_user_model().objects.get(pk=4)

    def test_update_user_admin(self):
        self.client.login(username='admin', password='admin@1234')
        self.client.patch(self.get_update_url(), {'username': 'apitester',
                                                  'email': 'mail@test.com'})
        updated = self.get_updated_user()
        self.assertEqual(updated.username, 'apitester')
        self.assertEqual(updated.email, 'mail@test.com')

    def test_update_user_owner(self):
        self.client.login(username='owneruser', password='edit@1234')
        self.client.patch(self.get_update_url(), {'username': 'apitester',
                                                  'email': 'mail@test.com'})
        updated = self.get_updated_user()
        self.assertEqual(updated.username, 'apitester')
        self.assertEqual(updated.email, 'mail@test.com')

    def test_update_user_unauthenticated(self):
        self.client.patch(self.get_update_url(), {'username': 'apitester',
                                                  'email': 'mail@test.com'})
        updated = self.get_updated_user()
        self.assertNotEqual(updated.email, 'mail@test.com')

    def test_update_user_non_owner(self):
        self.client.login(username='nonowneruser', password='temp@1234')
        self.client.patch(self.get_update_url(), {'username': 'apitester',
                                                  'email': 'mail@test.com'})
        updated = self.get_updated_user()
        self.assertNotEqual(updated.username, 'apitester')
        self.assertNotEqual(updated.email, 'mail@test.com')


class UserListTests(APITestCase):
    fixtures = ['users_data']

    def test_list_users(self):
        response = self.client.get(reverse('api:users-list'))
        self.assertEqual(response.status_code, 200)
