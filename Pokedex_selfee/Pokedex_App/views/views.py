from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..service import get_pokemon_data


@login_required
def get_pokemon_view(request, pokemon_name):
    pokemon_data = get_pokemon_data(pokemon_name)
    if pokemon_data is None:
        return JsonResponse({'error': 'Pokémon non trouvé'}, status=404)

    user_group_names = set(request.user.groups.values_list('name', flat=True))
    filtered_types = [
        type_entry
        for type_entry in pokemon_data.get('types', [])
        if type_entry.get('type', {}).get('name') in user_group_names
    ]

    filtered_payload = dict(pokemon_data)
    filtered_payload['types'] = filtered_types

    return JsonResponse(filtered_payload, status=200)