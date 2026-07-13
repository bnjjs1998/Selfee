from django.urls import path
from Pokedex_selfee.Pokedex_App.views.types_pokemonviews import UserGroupAddView, UserGroupRemoveView


urlpatterns = [
    path('group/<str:pokemon_type>/add/', UserGroupAddView.as_view(), name='add_pokemon_type'),
    path('group/<str:pokemon_type>/remove/', UserGroupRemoveView.as_view(), name='remove_pokemon_type'),
]


# path('group/<str:pokemon_type>/add/', PokemonViewFTypes.as_view(), name='add_pokemon_type'),