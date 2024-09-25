import json
import os
from game.player import Player
from pokemon import Pokemon


class SaveLoadManager:
    SAVE_FILE = 'savegame.json'

    @staticmethod
    def get_save_file_path():
        """Devuelve la ruta absoluta del archivo de guardado."""
        save_folder = os.path.join(os.getcwd(), 'data')
        os.makedirs(save_folder, exist_ok=True)
        return os.path.join(save_folder, SaveLoadManager.SAVE_FILE)

    @staticmethod
    def save_game(player):
        """Guarda el estado del jugador y sus Pokémon en un archivo JSON."""
        save_file_path = SaveLoadManager.get_save_file_path()

        # Preparar los datos del jugador para guardarlos
        player_data = {
            'player_name': player.name,
            'badges': player.badges,
            'money': player.money,
            'pokedex_seen': list(player.pokedex_seen),  # Convertir el set a lista
            'pokedex_captured': list(player.pokedex_captured),  # Convertir el set a lista
            'playtime_seconds': player.playtime_seconds,
            'pokemons': [SaveLoadManager.serialize_pokemon(pokemon) for pokemon in player.pokemons]
        }

        # Guardar los datos en un archivo JSON
        with open(save_file_path, 'w') as save_file:
            json.dump(player_data, save_file, indent=4)

    @staticmethod
    def load_game():
        """Carga el estado del jugador y sus Pokémon desde un archivo JSON."""
        save_file_path = SaveLoadManager.get_save_file_path()

        # Verificar si existe un archivo de guardado
        if not os.path.exists(save_file_path):
            return None  # No hay datos guardados

        with open(save_file_path, 'r') as save_file:
            data = json.load(save_file)

        return SaveLoadManager.deserialize_player(data)

    @staticmethod
    def serialize_pokemon(pokemon):
        """Convierte un objeto Pokémon en un formato serializable (diccionario)."""
        try:
            return {
                'name': pokemon.name,
                'level': pokemon.level,
                'types': pokemon.types,
                'base_stats': pokemon.base_stats,
                'evs': pokemon.evs,
                'ivs': pokemon.ivs,  # Verifica que ivs sea serializable
                'current_stats': pokemon.current_stats,  # Verifica que current_stats sea serializable
                'current_hp': pokemon.current_hp,
                'experience': pokemon.experience,
                'experience_to_next_level': pokemon.experience_to_next_level,
                'moves': pokemon.moves,
                'height': pokemon.height,
                'weight': pokemon.weight,
                'status': pokemon.status,
                'id': pokemon.id,
            }
        except Exception as e:
            print(f"Error serializing pokemon {pokemon.name}: {e}")
            raise

    @staticmethod
    def deserialize_pokemon(pokemon_data):
        """Convierte un diccionario JSON en un objeto Pokémon."""
        pokemon = Pokemon(
            name=pokemon_data['name'],
            types=pokemon_data['types'],
            base_stats=pokemon_data['base_stats'],
            evs=pokemon_data['evs'],
            moves=pokemon_data['moves'],
            height=pokemon_data['height'] * 10,  # Convertir a decímetros
            weight=pokemon_data['weight'] * 10,  # Convertir a hectogramos
            level=pokemon_data['level'],
            status=pokemon_data['status']
        )
        pokemon.ivs = pokemon_data['ivs']
        pokemon.current_stats = pokemon_data['current_stats']
        pokemon.current_hp = pokemon_data['current_hp']
        pokemon.experience = pokemon_data['experience']
        pokemon.experience_to_next_level = pokemon_data['experience_to_next_level']
        pokemon.id = pokemon_data['id']

        return pokemon

    @staticmethod
    def deserialize_player(data):
        """Deserializa los datos del jugador y crea un objeto 'Player'."""
        player = Player(name=data['player_name'])
        player.badges = data['badges']
        player.money = data['money']
        player.pokedex_seen = set(data['pokedex_seen'])
        player.pokedex_captured = set(data['pokedex_captured'])
        player.playtime_seconds = data['playtime_seconds']
        player.pokemons = [SaveLoadManager.deserialize_pokemon(pokemon_data) for pokemon_data in data['pokemons']]

        return player

