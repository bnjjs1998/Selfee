from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
