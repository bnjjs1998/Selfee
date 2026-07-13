import requests
import re

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None


def get_pokemon_list_by_types_service(type_names):
    pokemon_by_id = {}

    for type_name in type_names:
        url = f"https://pokeapi.co/api/v2/type/{type_name}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            return {"error": "Impossible de contacter PokeAPI"}

        if response.status_code != 200:
            continue

        data = response.json()
        for item in data.get("pokemon", []):
            pokemon_ref = item.get("pokemon", {})
            pokemon_name = pokemon_ref.get("name")
            pokemon_url = pokemon_ref.get("url", "")

            match = re.search(r"/pokemon/(\d+)/?$", pokemon_url)
            if not pokemon_name or not match:
                continue

            pokemon_id = int(match.group(1))
            pokemon_by_id[pokemon_id] = {
                "id": pokemon_id,
                "name": pokemon_name,
            }

    return [pokemon_by_id[key] for key in sorted(pokemon_by_id.keys())]
