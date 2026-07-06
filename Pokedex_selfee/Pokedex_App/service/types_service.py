import requests


def get_typespokemon_data(pokemon_type):
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        return None

    if response.status_code == 200:
        return response.json()
    return None


def add_pokemon_type_service(pokemon_type):
    """Return data for a pokemon type: {'type': name, 'pokemons': [names]} or {'error': msg}.

    Uses the public pokeapi to fetch the type and lists associated pokemon names.
    """
    if not pokemon_type:
        return {"error": "Type non précisé"}

    data = get_typespokemon_data(pokemon_type)
    if data is None:
        return {"error": "Type de Pokémon introuvable"}

    type_name = data.get("name")
    pokemon_entries = data.get("pokemon", [])
    pokemon_names = []
    for entry in pokemon_entries:
        p = entry.get("pokemon")
        if isinstance(p, dict) and "name" in p:
            pokemon_names.append(p["name"])

    return {"type": type_name, "pokemons": pokemon_names}


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
