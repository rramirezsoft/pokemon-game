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
                delay *= 2
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
            return {
                'name': move_data['name'],
                'type': move_data['type']['name'],
                'power': move_data['power'] if move_data['power'] else "N/A",
                'pp': move_data['pp'],
                'accuracy': move_data['accuracy'] if move_data['accuracy'] else "N/A",
                'damage_class': move_data['damage_class']['name'],
                'description': move_data['effect_entries'][0]['short_effect']
                if move_data['effect_entries'] else "No description available"
            }
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
                        moves.append({
                            'name': move_name,
                            'level': level_learned,
                            **move_details
                        })
    return moves


def get_pokemon_stats(pokemon_data):
    """Obtiene las estadísticas base y los EVs del Pokémon"""
    return {stat['stat']['name']: {
        'base_stat': stat['base_stat'],
        'evs': stat['effort']
    } for stat in pokemon_data['stats']}


def get_pokemon_types(pokemon_data):
    """Obtiene los tipos del Pokémon"""
    return [type_['type']['name'] for type_ in pokemon_data['types']]


def get_pokemon_physical_attributes(pokemon_data):
    """Obtiene la altura y el peso del Pokémon"""
    return {"height": pokemon_data['height'], "weight": pokemon_data['weight']}


def get_pokemon_species_data(pokemon_id, retries=3, delay=5):
    """Obtiene información adicional de la especie del Pokémon"""
    url = f"{POKEAPI_SPECIES_URL}{pokemon_id}"
    for i in range(retries):
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
            species_data = response.json()

            # Extraer datos de la especie
            return {
                'is_legendary': species_data.get('is_legendary', False),
                'is_mythical': species_data.get('is_mythical', False),
                'capture_rate': species_data.get('capture_rate', 0),
                'gender_rate': species_data.get('gender_rate', -1),  # -1 indica género desconocido
                'description': next((entry['flavor_text'] for entry in species_data['flavor_text_entries']
                                     if entry['language']['name'] == 'en'), "Description not available."),
                'evolution_chain': get_evolution_chain(species_data['evolution_chain']['url'])
            }

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


def get_evolution_chain(evolution_chain_url, retries=3, delay=5):
    """Obtiene la cadena evolutiva del Pokémon"""
    for i in range(retries):
        try:
            response = session.get(evolution_chain_url, timeout=15)
            response.raise_for_status()
            chain_data = response.json()
            evolutions = []
            current_stage = chain_data['chain']
            while current_stage:
                evolution_details = current_stage['evolves_to']
                evolves_to = []
                for evo in evolution_details:
                    # Verificar si 'evolution_details' existe y tiene elementos
                    if evo['evolution_details']:
                        evo_details = evo['evolution_details'][0]  # Solo tomamos el primer detalle
                        evolves_to.append({
                            'name': evo['species']['name'],
                            'min_level': evo_details.get('min_level'),
                            'trigger': evo_details.get('trigger', {}).get('name'),
                            'item': evo_details.get('item', {}).get('name') if evo_details.get('item') else None
                        })
                    else:
                        evolves_to.append({
                            'name': evo['species']['name'],
                            'min_level': None,
                            'trigger': None,
                            'item': None
                        })
                evolutions.append({
                    'name': current_stage['species']['name'],
                    'evolves_to': evolves_to
                })
                current_stage = evolution_details[0] if evolution_details else None
            return evolutions
        except requests.exceptions.Timeout:
            if i < retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                return None
        except requests.exceptions.RequestException:
            return None


def get_pokemon_abilities(pokemon_data, retries=3, delay=5):
    """Obtiene las habilidades y sus efectos."""
    abilities = []
    for ability in pokemon_data['abilities']:
        ability_name = ability['ability']['name']
        url = ability['ability']['url']
        for i in range(retries):
            try:
                response = session.get(url, timeout=15)
                response.raise_for_status()
                effect = next((entry['effect'] for entry in response.json()['effect_entries']
                               if entry['language']['name'] == 'en'), "No effect available")
                abilities.append({'name': ability_name, 'effect': effect})
                break  # Rompe el ciclo si se realiza la solicitud sin errores
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener habilidad {ability_name}: {e}")
                if i < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    print(f"Se omitió la habilidad {ability_name} después de varios intentos.")
                    abilities.append({'name': ability_name, 'effect': "No effect available"})
                    break
    return abilities


def download_file(url, file_name, save_directory):
    """Descarga un archivo desde una URL y lo guarda."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for i in range(3):  # Intentos para descargar el archivo
        try:
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                file_path = os.path.join(save_directory, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Archivo {file_name} descargado.")
                return True  # Indica que la descarga fue exitosa
            else:
                print(f"Error al descargar el archivo {file_name}. Código de estado: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Timeout al descargar el archivo {file_name}.")
            if i < 2:
                print("Reintentando en 5 segundos...")
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar el archivo {file_name}: {e}")
            break
    return False  # Indica que la descarga falló


def download_pokemon_image(pokemon_id, pokemon_name, save_directory='../assets/pokemon_images'):
    """Descargar la imagen de un Pokémon y guardarla."""
    url = (f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/"
           f"pokemon/other/official-artwork/{pokemon_id}.png")
    file_name = f"{pokemon_name.lower()}.png"
    download_file(url, file_name, save_directory)


def download_pokemon_sound(pokemon_name, save_directory='../assets/pokemon_sounds'):
    """Descarga el sonido de un Pokémon y lo guarda."""
    sound_url = f"https://play.pokemonshowdown.com/audio/cries/{pokemon_name}.mp3"
    if sound_url:
        file_name = f"{pokemon_name.lower().split('-')[0]}.mp3"
        download_file(sound_url, file_name, save_directory)
    else:
        print(f"No se pudo descargar el sonido del Pokémon {pokemon_name}.")


def collect_pokemon_info(pokemon_name_or_id):
    """Recoge toda la información relevante de un Pokémon"""
    pokemon_data = get_pokemon_data(pokemon_name_or_id)
    if pokemon_data:
        species_data = get_pokemon_species_data(pokemon_data['id'])

        pokemon_info = {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'].split('-')[0],
            'types': get_pokemon_types(pokemon_data),
            'abilities': get_pokemon_abilities(pokemon_data),
            'stats': get_pokemon_stats(pokemon_data),
            'moves': get_pokemon_moves(pokemon_data),
            'physical_attributes': get_pokemon_physical_attributes(pokemon_data),
            'species': species_data,
            'image_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_data['id']}.png",
            'sound_url':f"https://play.pokemonshowdown.com/audio/cries/{pokemon_data['name']}.mp3"
        }
        return pokemon_info, pokemon_data['id']
    else:
        return None


def collect_pokemon():
    """Recoge y guarda los datos de los Pokémon de las generaciones 1 a 5"""
    all_pokemon_data = []
    for pokemon_id in range(1, 650):
        print(f"Obteniendo datos del Pokémon con ID {pokemon_id}...")
        pokemon_info, pokemon_api_id = collect_pokemon_info(pokemon_id)
        if pokemon_info:
            all_pokemon_data.append(pokemon_info)
            print(f"Datos del Pokémon con ID {pokemon_id} obtenidos con éxito.")
        time.sleep(1)

    with open("data/poke_data.json", 'w') as file:
        json.dump(all_pokemon_data, file, indent=4)

    print("Datos de los Pokémon guardados en 'poke_data.json'")



if __name__ == '__main__':
    collect_pokemon()


