from unittest.mock import Mock, patch

from django.test import TestCase

from Pokedex_selfee.Pokedex_App.service.poke_name_service import (
	get_pokemon_data,
	get_pokemon_list_by_types_service,
)
from Pokedex_selfee.Pokedex_App.service.types_service import get_all_types_service


class PokemonServiceTests(TestCase):
	@patch('Pokedex_selfee.Pokedex_App.service.poke_name_service.requests.get')
	def test_get_pokemon_data_success(self, mock_get):
		response = Mock()
		response.status_code = 200
		response.json.return_value = {'name': 'bulbasaur'}
		mock_get.return_value = response

		data = get_pokemon_data('bulbasaur')

		self.assertEqual(data, {'name': 'bulbasaur'})

	@patch('Pokedex_selfee.Pokedex_App.service.poke_name_service.requests.get')
	def test_get_pokemon_data_not_found(self, mock_get):
		response = Mock()
		response.status_code = 404
		mock_get.return_value = response

		data = get_pokemon_data('missingno')

		self.assertIsNone(data)

	@patch('Pokedex_selfee.Pokedex_App.service.poke_name_service.requests.get')
	def test_get_pokemon_list_by_types_service_deduplicates_and_sorts(self, mock_get):
		grass_response = Mock()
		grass_response.status_code = 200
		grass_response.json.return_value = {
			'pokemon': [
				{'pokemon': {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'}},
				{'pokemon': {'name': 'oddish', 'url': 'https://pokeapi.co/api/v2/pokemon/43/'}},
			]
		}

		fire_response = Mock()
		fire_response.status_code = 200
		fire_response.json.return_value = {
			'pokemon': [
				{'pokemon': {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'}},
				{'pokemon': {'name': 'charmander', 'url': 'https://pokeapi.co/api/v2/pokemon/4/'}},
			]
		}

		mock_get.side_effect = [grass_response, fire_response]

		data = get_pokemon_list_by_types_service(['grass', 'fire'])

		self.assertEqual(data, [
			{'id': 1, 'name': 'bulbasaur'},
			{'id': 4, 'name': 'charmander'},
			{'id': 43, 'name': 'oddish'},
		])

	@patch('Pokedex_selfee.Pokedex_App.service.poke_name_service.requests.get')
	def test_get_pokemon_list_by_types_service_request_exception(self, mock_get):
		import requests

		mock_get.side_effect = requests.exceptions.RequestException()
		data = get_pokemon_list_by_types_service(['grass'])

		self.assertEqual(data, {'error': 'Impossible de contacter PokeAPI'})


class TypesServiceTests(TestCase):
	@patch('Pokedex_selfee.Pokedex_App.service.types_service.requests.get')
	def test_get_all_types_service_success(self, mock_get):
		response = Mock()
		response.status_code = 200
		response.json.return_value = {
			'results': [
				{'name': 'grass'},
				{'name': 'fire'},
			]
		}
		mock_get.return_value = response

		data = get_all_types_service()

		self.assertEqual(data, {'types': ['grass', 'fire']})

	@patch('Pokedex_selfee.Pokedex_App.service.types_service.requests.get')
	def test_get_all_types_service_http_error(self, mock_get):
		response = Mock()
		response.status_code = 500
		mock_get.return_value = response

		data = get_all_types_service()

		self.assertEqual(data, {'error': 'Erreur lors de la récupération des types'})

	@patch('Pokedex_selfee.Pokedex_App.service.types_service.requests.get')
	def test_get_all_types_service_request_exception(self, mock_get):
		import requests

		mock_get.side_effect = requests.exceptions.RequestException()
		data = get_all_types_service()

		self.assertEqual(data, {'error': "Impossible de contacter l'API pokeapi"})
