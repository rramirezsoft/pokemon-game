import os
import requests
import json
import time

# URLs base de la PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEAPI_MOVE_URL = "https://pokeapi.co/api/v2/move/"
POKEAPI_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"

# Generación y grupo de versión que vamos a utilizar
VERSION_GROUP = 'black-white'

# Configuración de la sesión de requests
session = requests.Session()
session.headers.update({'User-Agent': 'PokeAPI Client'})

def get_pokemon_data(pokemon_name_or_id, retries=3, delay=5):
    """Obtiene los datos básicos de un Pokémon"""
    url = f"{POKEAPI_BASE_URL}{pokemon_name_or_id}"
    for i in range(retries):
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout al obtener datos del Pokémon {pokemon_name_or_id}.")
            if i < retries - 1:
                print(f"Reintentando en {delay} segundos... (Intento {i + 1}/{retries})")
                time.sleep(delay)
                delay *= 2  # Duplicar el tiempo de espera
            else:
                print("Error persistente al obtener datos del Pokémon después de varios intentos.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos del Pokémon {pokemon_name_or_id}: {e}")
            return None


def get_move_details(move_url, retries=3, delay=5):
    """Obtiene los detalles de un movimiento y añade su descripción"""
    for i in range(retries):
        try:
            response = session.get(move_url, timeout=15)
            response.raise_for_status()
            move_data = response.json()
            move_details = {
                'name': move_data['name'],
                'type': move_data['type']['name'],
                'power': move_data['power'] if move_data['power'] else "N/A",
                'pp': move_data['pp'],
                'accuracy': move_data['accuracy'] if move_data['accuracy'] else "N/A",
                'damage_class': move_data['damage_class']['name'],
                'description': move_data['effect_entries'][0]['short_effect']
                if move_data['effect_entries'] else "No description available"
            }
            return move_details
        except requests.exceptions.Timeout:
            print("Timeout al obtener los detalles del movimiento.")
            if i < retries - 1:
                print(f"Reintentando en {delay} segundos... (Intento {i + 1}/{retries})")
                time.sleep(delay)
                delay *= 2
            else:
                print("Error persistente al obtener los detalles del movimiento después de varios intentos.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los detalles del movimiento: {e}")
            return None


def get_pokemon_moves(pokemon_data):
    """Obtiene los movimientos del Pokémon filtrados por la versión de la quinta generación"""
    moves = []
    seen_moves = set()  # Usamos un conjunto para evitar duplicados
    for move in pokemon_data['moves']:
        for version_detail in move['version_group_details']:
            if (version_detail['move_learn_method']['name'] == 'level-up'
                    and version_detail['version_group']['name'] == VERSION_GROUP):
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
                            'damage_class': move_details['damage_class'],
                            'description': move_details['description']
                        }
                        moves.append(move_info)
    return moves


def get_pokemon_stats(pokemon_data):
    """Obtiene las estadísticas base y los EVs del Pokémon"""
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
    """Obtiene los tipos del Pokémon"""
    types = [type_['type']['name'] for type_ in pokemon_data['types']]
    return types


def get_pokemon_physical_attributes(pokemon_data):
    """Obtiene la altura y el peso del Pokémon"""
    height = pokemon_data['height']
    weight = pokemon_data['weight']
    return {"height": height, "weight": weight}


def get_pokemon_species_data(pokemon_id, retries=3, delay=5):
    """Obtiene información adicional de la especie del Pokémon, incluyendo si es legendario"""
    url = f"{POKEAPI_SPECIES_URL}{pokemon_id}"
    for i in range(retries):
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout al obtener datos de la especie del Pokémon {pokemon_id}.")
            if i < retries - 1:
                print(f"Reintentando en {delay} segundos... (Intento {i + 1}/{retries})")
                time.sleep(delay)
                delay *= 2
            else:
                print("Error persistente al obtener datos de la especie después de varios intentos.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de la especie del Pokémon {pokemon_id}: {e}")
            return None


def download_pokemon_image(pokemon_id, pokemon_name, save_directory='../assets/pokemon_images'):
    """Descargar la imagen de un Pokémon y guardarla con su nombre en el directorio especificado."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # URL para descargar la imagen oficial del artwork del Pokémon
    url = (f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/"
           f"pokemon/other/official-artwork/{pokemon_id}.png")

    for i in range(3):  # Intentos para descargar la imagen
        try:
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                image_path = os.path.join(save_directory, f"{pokemon_name.lower()}.png")
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                print(f"Imagen del Pokémon {pokemon_name} descargada.")
                break
            else:
                print(f"Error al descargar la imagen del Pokémon {pokemon_name}. "
                      f"Código de estado: {response.status_code}")
        except requests.exceptions.Timeout:
            print("Timeout al descargar la imagen.")
            if i < 2:
                print("Reintentando en 5 segundos...")
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen del Pokémon {pokemon_name}: {e}")
            break


def collect_pokemon_info(pokemon_name_or_id):
    """Recoge toda la información relevante de un Pokémon"""
    pokemon_data = get_pokemon_data(pokemon_name_or_id)
    if pokemon_data:
        species_data = get_pokemon_species_data(pokemon_data['id'])
        is_legendary = species_data['is_legendary'] if species_data else False

        pokemon_info = {
            'id': pokemon_data['id'],  # Número de la Pokedex
            'name': pokemon_data['name'],
            'types': get_pokemon_types(pokemon_data),
            'stats': get_pokemon_stats(pokemon_data),
            'moves': get_pokemon_moves(pokemon_data),
            'physical_attributes': get_pokemon_physical_attributes(pokemon_data),
            'image_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official"
                         f"-artwork/{pokemon_data['id']}.png",
            'is_legendary': is_legendary
        }
        return pokemon_info, pokemon_data['id']
    else:
        return None, None


def collect_pokemon():
    """Recoge y guarda los datos de los Pokémon de las generaciones 1 a 5"""
    all_pokemon_data = []
    for pokemon_id in range(1, 650):  # Pokémon hasta la quinta generación (649 Pokémon)
        print(f"Obteniendo datos del Pokémon con ID {pokemon_id}...")
        pokemon_info, pokemon_api_id = collect_pokemon_info(pokemon_id)
        if pokemon_info:
            all_pokemon_data.append(pokemon_info)
            download_pokemon_image(pokemon_api_id, pokemon_info['name'])

    # Guardar la información en un archivo JSON
    with open("data/poke_data.json", 'w') as file:
        json.dump(all_pokemon_data, file, indent=4)

    print("Datos de los Pokémon de las generaciones 1 a 5 guardados en 'poke_data.json'")


if __name__ == "__main__":
    collect_pokemon()

