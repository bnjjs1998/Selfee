def filter_pokemon_types_by_groups(pokemon_data, user_group_names):
    filtered_types = [
        type_entry
        for type_entry in pokemon_data.get('types', [])
        if type_entry.get('type', {}).get('name') in user_group_names
    ]

    filtered_payload = dict(pokemon_data)
    filtered_payload['types'] = filtered_types
    return filtered_payload
