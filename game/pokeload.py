import requests
import json
import time
import os

# URL base de la PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEAPI_MOVE_URL = "https://pokeapi.co/api/v2/move/"


def get_pokemon_data(pokemon_name_or_id, retries=3, delay=5):
    url = f"{POKEAPI_BASE_URL}{pokemon_name_or_id}"
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos del Pokémon {pokemon_name_or_id}: {e}")
            if i < retries - 1:
                print(f"Reintentando en {delay} segundos... (Intento {i + 1}/{retries})")
                time.sleep(delay)
            else:
                print("Error persistente al obtener datos del Pokémon después de varios intentos.")
                return None


def get_move_details(move_url, retries=3, delay=5):
    for i in range(retries):
        try:
            response = requests.get(move_url, timeout=10)
            response.raise_for_status()
            move_data = response.json()
            move_details = {
                'name': move_data['name'],
                'type': move_data['type']['name'],
                'power': move_data['power'] if move_data['power'] else "N/A",
                'pp': move_data['pp'],
                'accuracy': move_data['accuracy'] if move_data['accuracy'] else "N/A",
                'damage_class': move_data['damage_class']['name']
            }
            return move_details
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los detalles del movimiento: {e}")
            if i < retries - 1:
                print(f"Reintentando en {delay} segundos... (Intento {i + 1}/{retries})")
                time.sleep(delay)
            else:
                print("Error persistente al obtener los detalles del movimiento después de varios intentos.")
                return None


def get_pokemon_moves(pokemon_data):
    moves = []
    seen_moves = set()  # Usamos un conjunto para evitar duplicados
    for move in pokemon_data['moves']:
        for version_detail in move['version_group_details']:
            if (version_detail['move_learn_method']['name'] == 'level-up'
                    and version_detail['version_group']['name'] == 'red-blue'):
                move_name = move['move']['name']
                if move_name not in seen_moves:
                    seen_moves.add(move_name)
                    move_url = move['move']['url']
                    level_learned = version_detail['level_learned_at']
                    move_details = get_move_details(move_url)
                    if move_details:
                        move_info = {
                            'name': move_name,
                            'level': level_learned,
                            'type': move_details['type'],
                            'power': move_details['power'],
                            'pp': move_details['pp'],
                            'accuracy': move_details['accuracy'],
                            'damage_class': move_details['damage_class']
                        }
                        moves.append(move_info)
    return moves


def get_pokemon_stats(pokemon_data):
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


def get_pokemon_types(pokemon_data):
    types = [type_['type']['name'] for type_ in pokemon_data['types']]
    return types


def get_pokemon_physical_attributes(pokemon_data):
    height = pokemon_data['height']
    weight = pokemon_data['weight']
    return {"height": height, "weight": weight}


def download_pokemon_image(pokemon_id, pokemon_name, save_directory='../assets/pokemon_images'):
    """Descargar la imagen de un Pokémon y guardarla con su nombre en el directorio especificado."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # URL para descargar la imagen oficial del artwork del Pokémon
    url = (f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/"
           f"pokemon/other/official-artwork/{pokemon_id}.png")

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        image_path = os.path.join(save_directory, f"{pokemon_name.lower()}.png")
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Imagen del Pokémon {pokemon_name} descargada.")
    else:
        print(f"Error al descargar la imagen del Pokémon {pokemon_name}. Código de estado: {response.status_code}")


def collect_pokemon_info(pokemon_name_or_id):
    pokemon_data = get_pokemon_data(pokemon_name_or_id)
    if pokemon_data:
        pokemon_info = {
            'name': pokemon_data['name'],
            'types': get_pokemon_types(pokemon_data),
            'stats': get_pokemon_stats(pokemon_data),
            'moves': get_pokemon_moves(pokemon_data),
            'physical_attributes': get_pokemon_physical_attributes(pokemon_data),
            'image_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official"
                         f"-artwork/{pokemon_data['id']}.png"
        }
        return pokemon_info, pokemon_data['id']
    else:
        return None, None


def collect_pokemon():
    all_pokemon_data = []
    for pokemon_id in range(1, 151):
        print(f"Obteniendo datos del Pokémon con ID {pokemon_id}...")
        pokemon_info, pokemon_api_id = collect_pokemon_info(pokemon_id)
        if pokemon_info:
            all_pokemon_data.append(pokemon_info)
            download_pokemon_image(pokemon_api_id, pokemon_info['name'])

    with open("data/pokemon_data.json", 'w') as file:
        json.dump(all_pokemon_data, file, indent=4)

    print("Datos de los 150 primeros Pokémon guardados en 'pokemon_data.json'")

