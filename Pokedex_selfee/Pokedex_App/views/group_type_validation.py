from ..service.types_service import get_all_types_service


def is_valid_pokemon_type(pokemon_type):
    response = get_all_types_service()
    if "error" in response:
        return None

    available_types = set(response.get("types", []))
    return pokemon_type.lower() in available_types
