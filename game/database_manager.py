from pymongo import MongoClient
from game.pokemon import Pokemon
from dotenv import load_dotenv
import os

load_dotenv()  # Cargamos las variables de entorno del archivo .env

# Obtenemos la URI de MongoDB desde las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")


def serialize_pokemon(pokemon):
    """Convierte un objeto Pokemon en un diccionario para guardarlo."""
    return {
        "pokedex_id": pokemon.pokedex_id,
        "id": pokemon.random_id,
        "name": pokemon.name,
        "level": pokemon.level,
        "types": pokemon.types,
        "ability": pokemon.ability,
        "base_stats": pokemon.base_stats,
        'evs': pokemon.evs,
        'ivs': pokemon.ivs,
        'experience': pokemon.experience,
        'moves': pokemon.moves,
        'height': pokemon.height,
        'weight': pokemon.weight,
        'gender': pokemon.gender,
        'status': pokemon.status,
    }


def deserialize_pokemon(data):
    return Pokemon(
        name=data['name'],
        types=data['types'],
        abilities=[data['ability']],
        base_stats=data['base_stats'],
        evs=data['evs'],
        moves=data['moves'],
        height=data['height'],
        weight=data['weight'],
        gender_rate=data['gender'],
        pokedex_id=data['pokedex_id'],
        random_id=data['id'],
        experience=data.get('experience', 0),
        level=data.get('level', None),
        ivs=data.get('ivs', None),
        status=data.get('status', None)
    )


class DataBaseManager:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.PokeDataBase
        self.collection = self.db.players

    def player_id_exists(self, player_id):
        """Verifica si el ID del jugador ya existe en la base de datos."""
        existing_player = self.collection.find_one({"player_id": player_id})
        return existing_player is not None

    def save_player(self, player):
        """Guardar objeto en la base de datos"""
        # Creamos el documento
        player_data = {
            "player_id": player.player_id,
            "name": player.name,
            "money": player.money,
            "badges": player.badges,
            "playtime_seconds": player.playtime_seconds,
            "pokedex_seen": list(player.pokedex_seen),
            "pokedex_captured": list(player.pokedex_captured),
            "items": player.bag.items,
            "pokemons": [serialize_pokemon(pokemon) for pokemon in player.pokemons],
            "pc": [serialize_pokemon(pokemon) for pokemon in player.pc],
        }

        # Guardamos el documento en base de datos
        self.collection.update_one(
            {"player_id": player.player_id},
            {"$set": player_data},
            upsert=True
        )

        # Guardamos el ID del jugador en un archivo local para su posterior lectura
        with open("data/player_id.txt", "w") as f:
            f.write(str(player.player_id))

    @staticmethod
    def load_player(player_data):
        """
        Carga un jugador desde los datos proporcionados por la base de datos.
        :param player_data: Los datos del jugador recuperados de la base de datos.
        :return: Un objeto Player con la información deserializada.
        """
        from game.player import Player

        # Crear una instancia del jugador con el nombre y el ID
        player = Player(name=player_data['name'])
        player.player_id = player_data['player_id']
        player.money = player_data['money']
        player.badges = player_data['badges']
        player.playtime_seconds = player_data['playtime_seconds']
        player.pokedex_seen = set(player_data['pokedex_seen'])
        player.pokedex_captured = set(player_data['pokedex_captured'])
        player.bag.items = player_data['items']  # Suponiendo que Bag tiene un atributo 'items'

        # Deserializar Pokémon en el equipo y en el PC
        player.pokemons = [deserialize_pokemon(pokemon) for pokemon in player_data['pokemons']]
        player.pc = [deserialize_pokemon(pokemon) for pokemon in player_data['pc']]

        return player

    @staticmethod
    def get_saved_player_id():
        """Lee el archivo player_id.txt para obtener el ID del jugador guardado."""
        try:
            with open("data/player_id.txt", "r") as file:
                player_id = file.read().strip()
                if player_id:
                    return player_id
        except FileNotFoundError:
            return None
        return None
