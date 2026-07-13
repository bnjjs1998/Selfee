from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token


class HelloWorldViewTests(TestCase):

    def test_hello_world_route_returns_expected_response(self):
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello World !')


class LoginSessionTests(TestCase):

    def test_login_sets_session_cookie_and_auth_state(self):
        user = get_user_model().objects.create_user(username='alice', password='secret123')

        response = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'secret123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('sessionid', response.cookies)
        self.assertIn('token', response.json())

        auth_response = self.client.get(reverse('login'))
        self.assertEqual(auth_response.status_code, 200)
        self.assertTrue(auth_response.json()['authenticated'])

    def test_logout_clears_session(self):
        user = get_user_model().objects.create_user(username='alice', password='secret123')

        login_response = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'secret123',
        })
        self.assertEqual(login_response.status_code, 200)

        logout_response = self.client.post(reverse('logout'))
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json()['message'], 'Déconnexion réussie')

        session_response = self.client.get(reverse('session_status'))
        self.assertEqual(session_response.status_code, 401)
        self.assertEqual(session_response.json()['error'], 'Utilisateur non authentifié')

    def test_login_invalid_credentials(self):
        get_user_model().objects.create_user(username='alice', password='secret123')

        response = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'bad-pass',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Identifiants invalides')

    def test_session_with_token_authentication(self):
        user = get_user_model().objects.create_user(username='bob', password='secret123')
        token, _ = Token.objects.get_or_create(user=user)

        response = self.client.get(
            reverse('session_status'),
            HTTP_AUTHORIZATION=f'Token {token.key}',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['authenticated'])
        self.assertEqual(response.json()['username'], 'bob')

    def test_user_me_with_token_returns_groups(self):
        user = get_user_model().objects.create_user(username='charlie', password='secret123')
        token, _ = Token.objects.get_or_create(user=user)

        response = self.client.get(
            reverse('user_me'),
            HTTP_AUTHORIZATION=f'Token {token.key}',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_id'], user.pk)
        self.assertEqual(response.json()['username'], 'charlie')
        self.assertIn('user_groups', response.json())

    def test_user_me_requires_authentication(self):
        response = self.client.get(reverse('user_me'))
        self.assertEqual(response.status_code, 403)
