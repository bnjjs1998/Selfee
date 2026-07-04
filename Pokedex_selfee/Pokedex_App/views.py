from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .service import get_pokemon_data


@login_required
def get_pokemon_view(request, pokemon_name):
    data = get_pokemon_data(pokemon_name)
    if data is None:
        return JsonResponse({'error': 'Pokemon introuvable'}, status=404)
    return JsonResponse(data)