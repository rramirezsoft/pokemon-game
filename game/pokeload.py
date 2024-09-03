import requests
import json

# URL base de la PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


# Función para obtener los datos de un Pokémon en particular por su ID o nombre
def get_pokemon_data(pokemon_name_or_id):
    url = f"{POKEAPI_BASE_URL}{pokemon_name_or_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos del Pokémon {pokemon_name_or_id}. Código de estado: {response.status_code}")
        return None


# Función para obtener los movimientos con su nivel de desbloqueo sin duplicados
def get_pokemon_moves(pokemon_data):
    """
    Extrae una lista de los movimientos que puede aprender el Pokémon junto con el nivel en que se desbloquean,
    evitando movimientos duplicados.
    """
    moves = {}

    for move in pokemon_data['moves']:
        for version_detail in move['version_group_details']:
            # Filtramos para obtener los movimientos que se aprenden subiendo de nivel (move_learn_method = 'level-up')
            if version_detail['move_learn_method']['name'] == 'level-up':
                move_name = move['move']['name']
                level_learned = version_detail['level_learned_at']

                # Solo añadir si el movimiento no está registrado o si tiene un nivel menor (prioriza niveles más bajos)
                if move_name not in moves or level_learned < moves[move_name]:
                    moves[move_name] = level_learned

    # Convertimos el diccionario en una lista de movimientos con sus niveles
    return [{'name': name, 'level': level} for name, level in moves.items()]


# Función para obtener las estadísticas principales del Pokémon (incluyendo EVs)
def get_pokemon_stats(pokemon_data):
    """
    Extrae las estadísticas principales (HP, ataque, defensa, etc.) del Pokémon, incluyendo sus EVs.
    """
    stats = {}
    for stat in pokemon_data['stats']:
        stat_name = stat['stat']['name']
        base_stat = stat['base_stat']
        evs = stat['effort']
        stats[stat_name] = {
            'base_stat': base_stat,
            'evs': evs
        }
    return stats


# Función para obtener los tipos del Pokémon
def get_pokemon_types(pokemon_data):
    """
    Extrae los tipos del Pokémon (agua, fuego, planta, etc.).
    """
    types = [type_['type']['name'] for type_ in pokemon_data['types']]
    return types


# Función para obtener peso y altura del Pokémon
def get_pokemon_physical_attributes(pokemon_data):
    """
    Extrae el peso y la altura del Pokémon.
    """
    height = pokemon_data['height']
    weight = pokemon_data['weight']
    return {"height": height, "weight": weight}


# Guardar los datos en un archivo JSON
def save_pokemon_data(pokemon_data, filename="pokemon_data.json"):
    """
    Guarda los datos de un Pokémon en un archivo JSON.
    """
    with open(filename, 'w') as file:
        json.dump(pokemon_data, file, indent=4)
    print(f"Datos guardados en {filename}")


# Función principal que reúne toda la información relevante del Pokémon
def collect_pokemon_info(pokemon_name_or_id):
    pokemon_data = get_pokemon_data(pokemon_name_or_id)

    if pokemon_data:
        pokemon_info = {
            'name': pokemon_data['name'],
            'types': get_pokemon_types(pokemon_data),
            'stats': get_pokemon_stats(pokemon_data),
            'moves': get_pokemon_moves(pokemon_data),
            'physical_attributes': get_pokemon_physical_attributes(pokemon_data),
        }

        return pokemon_info
    else:
        return None


def collect_pokemon():
    all_pokemon_data = []

    # Iterar sobre los IDs del 1 al 150 para obtener los datos de los Pokémon de la generación 1
    for pokemon_id in range(1, 151):
        print(f"Obteniendo datos del Pokémon con ID {pokemon_id}...")
        pokemon_info = collect_pokemon_info(pokemon_id)

        if pokemon_info:
            all_pokemon_data.append(pokemon_info)

    # Guardar todos los datos en un archivo JSON
    with open("pokemon_data.json", 'w') as file:
        json.dump(all_pokemon_data, file, indent=4)

    print("Datos de los 150 primeros Pokémon guardados en 'first_150_pokemon_data.json'")

