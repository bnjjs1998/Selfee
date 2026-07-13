from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient


class PokemonListViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='pokeuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('Pokedex_selfee.Pokedex_App.views.pokemon_list_view.get_pokemon_list_by_types_service')
    def test_list_pokemons_by_user_groups(self, mock_service):
        Group.objects.get_or_create(name='grass')
        self.user.groups.add(Group.objects.get(name='grass'))

        mock_service.return_value = [
            {'id': 1, 'name': 'bulbasaur'},
            {'id': 2, 'name': 'ivysaur'},
        ]

        response = self.client.get('/api/pokemon/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'pokemons': [
                {'id': 1, 'name': 'bulbasaur'},
                {'id': 2, 'name': 'ivysaur'},
            ]
        })

    @patch('Pokedex_selfee.Pokedex_App.views.pokemon_list_view.get_pokemon_list_by_types_service')
    def test_list_pokemons_service_unavailable(self, mock_service):
        mock_service.return_value = {'error': 'Impossible de contacter PokeAPI'}

        response = self.client.get('/api/pokemon/')

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'error': 'Impossible de contacter PokeAPI'})

    @patch('Pokedex_selfee.Pokedex_App.views.pokemon_list_view.get_pokemon_list_by_types_service')
    def test_list_pokemons_passes_user_groups_to_service(self, mock_service):
        Group.objects.get_or_create(name='grass')
        Group.objects.get_or_create(name='fire')
        self.user.groups.add(Group.objects.get(name='grass'))
        self.user.groups.add(Group.objects.get(name='fire'))
        mock_service.return_value = []

        response = self.client.get('/api/pokemon/')

        self.assertEqual(response.status_code, 200)
        called_with = mock_service.call_args[0][0]
        self.assertEqual(set(called_with), {'grass', 'fire'})

    def test_list_pokemons_requires_authentication(self):
        unauth_client = APIClient()
        response = unauth_client.get('/api/pokemon/')
        self.assertEqual(response.status_code, 403)


class PokemonByNameViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='pokeuser2', password='password')
        Group.objects.get_or_create(name='grass')
        self.user.groups.add(Group.objects.get(name='grass'))
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('Pokedex_selfee.Pokedex_App.views.pokemon_by_name_view.get_pokemon_data')
    def test_get_pokemon_by_name_filters_types_by_user_groups(self, mock_get_data):
        mock_get_data.return_value = {
            'id': 1,
            'name': 'bulbasaur',
            'types': [
                {'type': {'name': 'grass'}},
                {'type': {'name': 'poison'}},
            ],
        }

        response = self.client.get('/api/pokemon/bulbasaur/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'bulbasaur')
        self.assertEqual(response.json()['types'], [{'type': {'name': 'grass'}}])

    @patch('Pokedex_selfee.Pokedex_App.views.pokemon_by_name_view.get_pokemon_data')
    def test_get_pokemon_by_name_not_found(self, mock_get_data):
        mock_get_data.return_value = None

        response = self.client.get('/api/pokemon/missingno/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Pokemon non trouve'})

    @patch('Pokedex_selfee.Pokedex_App.views.pokemon_by_name_view.get_pokemon_data')
    def test_get_pokemon_by_name_forbidden_when_no_matching_type(self, mock_get_data):
        mock_get_data.return_value = {
            'id': 4,
            'name': 'charmander',
            'types': [
                {'type': {'name': 'fire'}},
            ],
        }

        response = self.client.get('/api/pokemon/charmander/')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'error': 'Acces refuse a ce pokemon'})

    def test_get_pokemon_by_name_requires_authentication(self):
        unauth_client = APIClient()
        response = unauth_client.get('/api/pokemon/bulbasaur/')
        self.assertEqual(response.status_code, 403)
