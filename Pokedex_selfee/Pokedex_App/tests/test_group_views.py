from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from unittest.mock import patch


class GroupRoutesTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.group = Group.objects.create(name='grass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_add_group_success_via_post(self, mock_get_types):
        mock_get_types.return_value = {'types': ['grass', 'fire', 'water']}

        resp = self.client.post('/api/group/grass/add/')
        self.assertEqual(resp.status_code, 200)

        self.user.refresh_from_db()
        self.assertTrue(self.user.groups.filter(name='grass').exists())

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_add_group_invalid_type(self, mock_get_types):
        mock_get_types.return_value = {'types': ['grass', 'fire', 'water']}

        resp = self.client.post('/api/group/invalidtype/add/')
        self.assertEqual(resp.status_code, 404)

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_remove_group_success(self, mock_get_types):
        mock_get_types.return_value = {'types': ['grass', 'fire', 'water']}

        # add user to group then remove
        self.user.groups.add(self.group)
        resp = self.client.post(f'/api/group/{self.group.name}/remove/')
        self.assertEqual(resp.status_code, 200)

        # reload user groups
        self.user.refresh_from_db()
        self.assertFalse(self.user.groups.filter(name__iexact=self.group.name).exists())

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_remove_group_not_member(self, mock_get_types):
        mock_get_types.return_value = {'types': ['grass', 'fire', 'water']}

        # user not in group
        resp = self.client.post(f'/api/group/{self.group.name}/remove/')
        self.assertEqual(resp.status_code, 400)

    def test_add_group_requires_authentication(self):
        unauth_client = APIClient()
        resp = unauth_client.post('/api/group/grass/add/')
        self.assertEqual(resp.status_code, 403)

    def test_remove_group_requires_authentication(self):
        unauth_client = APIClient()
        resp = unauth_client.post('/api/group/grass/remove/')
        self.assertEqual(resp.status_code, 403)

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_add_group_service_unavailable(self, mock_get_types):
        mock_get_types.return_value = {'error': 'unavailable'}

        resp = self.client.post('/api/group/grass/add/')
        self.assertEqual(resp.status_code, 503)

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_remove_group_invalid_type(self, mock_get_types):
        mock_get_types.return_value = {'types': ['grass', 'fire', 'water']}

        resp = self.client.post('/api/group/electricity/remove/')
        self.assertEqual(resp.status_code, 404)

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_remove_group_service_unavailable(self, mock_get_types):
        mock_get_types.return_value = {'error': 'unavailable'}

        resp = self.client.post('/api/group/grass/remove/')
        self.assertEqual(resp.status_code, 503)

    @patch('Pokedex_selfee.Pokedex_App.views.group_type_validation.get_all_types_service')
    def test_remove_group_success_via_delete(self, mock_get_types):
        mock_get_types.return_value = {'types': ['grass', 'fire', 'water']}

        self.user.groups.add(self.group)
        resp = self.client.delete(f'/api/group/{self.group.name}/remove/')
        self.assertEqual(resp.status_code, 200)
