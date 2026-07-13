from django.urls import path
from Pokedex_selfee.Pokedex_App.views.pokemon_list_view import PokemonListView
from Pokedex_selfee.Pokedex_App.views.pokemon_by_name_view import PokemonByNameView
from Pokedex_selfee.Pokedex_App.views.user_group_add_view import UserGroupAddView
from Pokedex_selfee.Pokedex_App.views.user_group_remove_view import UserGroupRemoveView


urlpatterns = [
    path('pokemon/', PokemonListView.as_view(), name='list_pokemons'),
    path('pokemon/<str:pokemon_name>/', PokemonByNameView.as_view(), name='get_pokemon'),
    path('group/<str:pokemon_type>/add/', UserGroupAddView.as_view(), name='add_pokemon_type'),
    path('group/<str:pokemon_type>/remove/', UserGroupRemoveView.as_view(), name='remove_pokemon_type'),
]
