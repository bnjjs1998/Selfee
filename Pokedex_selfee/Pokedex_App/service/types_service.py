import requests
from django.contrib.auth.models import Group
from django.db import transaction


def get_typespokemon_data(pokemon_type):
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        return None

    if response.status_code == 200:
        return response.json()
    return None



def add_pokemon_type_service(user, pokemon_type):
    """
    Fonction protégée par @login_required.
    """
    if user is None or not user.is_authenticated:
        return {"error": "Utilisateur non authentifié"}

    if not pokemon_type:
        return {"error": "Type non précisé"}

    data = get_typespokemon_data(pokemon_type)
    if data is None:
        return {"error": "Type de Pokémon introuvable"}

    type_name = data.get("name")
    
    with transaction.atomic():
        group, created = Group.objects.get_or_create(name=type_name)
        user.groups.add(group)

    return {"type": type_name, "message": "Ajout au groupe réussi"}

def get_all_types_service():
    """Fetch and return the list of all Pokemon types (names) from pokeapi."""
    url = "https://pokeapi.co/api/v2/type/"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        return {"error": "Impossible de contacter l'API pokeapi"}

    if response.status_code != 200:
        return {"error": "Erreur lors de la récupération des types"}

    data = response.json()
    results = data.get("results", [])
    type_names = [t.get("name") for t in results if "name" in t]
    return {"types": type_names}
