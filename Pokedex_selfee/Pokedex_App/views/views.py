from django.http import JsonResponse
from ..service import get_pokemon_data

def get_pokemon_view(request, pokemon_name):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Utilisateur non authentifié'}, status=401)

    pokemon_data = get_pokemon_data(pokemon_name)
    if pokemon_data is None:
        return JsonResponse({'error': 'Pokémon non trouvé'}, status=404)

    return JsonResponse(pokemon_data, status=200)