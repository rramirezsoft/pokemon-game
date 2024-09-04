import json
import random
import os
from PIL import Image


class Pokemon:
    def __init__(self, name, types, base_stats, evs, moves, height, weight, level=None, status=None, image_url=None):
        self.name = name
        self.types = types
        self.base_stats = base_stats
        self.evs = evs
        self.ivs = self.generate_ivs()
        self.level = random.randint(5, 100) if level is None else level  # Nivel aleatorio si no se especifica
        self.moves = self.select_moves(moves)
        self.height = height / 10  # Conversión a metros
        self.weight = weight / 10  # Conversión a kilogramos
        self.experience = 0
        self.experience_to_next_level = self.calculate_exp_to_next_level()
        self.status = status
        self.image_url = image_url
        self.current_stats = self.calculate_stats()

    @staticmethod
    def generate_ivs():
        """Generar IVs aleatorios entre 0 y 31 para cada estadística."""
        return {
            "hp": random.randint(0, 31),
            "attack": random.randint(0, 31),
            "defense": random.randint(0, 31),
            "special-attack": random.randint(0, 31),
            "special-defense": random.randint(0, 31),
            "speed": random.randint(0, 31)
        }

    def select_moves(self, moves):
        """Seleccionar hasta 4 movimientos disponibles según el nivel del Pokémon."""
        available_moves = [move for move in moves if move['level'] <= self.level]
        return random.sample(available_moves, min(len(available_moves), 4))

    def calculate_stats(self):
        """Calcular las estadísticas del Pokémon basadas en su nivel, base stats, IVs y EVs."""
        calculated_stats = {}
        for stat_name, base_stat in self.base_stats.items():
            iv = self.ivs.get(stat_name, 0)
            ev = self.evs.get(stat_name, 0)
            calculated_stats[stat_name] = self.calculate_stat(stat_name, base_stat, iv, ev)
        return calculated_stats

    def calculate_stat(self, stat_name, base_stat, iv, ev):
        """Fórmula para calcular el stat final de una estadística específica."""
        if stat_name == "hp":
            return int((((2 * base_stat + iv + (ev / 4)) * self.level) / 100) + self.level + 10)
        else:
            return int((((2 * base_stat + iv + (ev / 4)) * self.level) / 100) + 5)

    def calculate_exp_to_next_level(self):
        """Calcular la experiencia necesaria para el siguiente nivel."""
        return 4 * (self.level ** 3) // 5

    def get_pokemon_info(self):
        """Devolver la información completa del Pokémon en un formato estructurado."""
        return {
            "name": self.name,
            "level": self.level,
            "types": self.types,
            "base_stats": self.base_stats,
            "ivs": self.ivs,
            "current_stats": self.current_stats,
            "height_m": self.height,
            "weight_kg": self.weight,
            "moves": self.moves,
            "image_url": self.image_url,
        }

    @classmethod
    def from_json(cls, pokemon_data):
        """Crear un Pokémon a partir de los datos en formato JSON."""
        name = pokemon_data['name']
        types = pokemon_data['types']
        base_stats = {stat_name: stat_info['base_stat'] for stat_name, stat_info in pokemon_data['stats'].items()}
        evs = {stat_name: stat_info['evs'] for stat_name, stat_info in pokemon_data['stats'].items()}
        moves = pokemon_data['moves']
        height = pokemon_data['physical_attributes']['height']
        weight = pokemon_data['physical_attributes']['weight']
        image_url = pokemon_data['image_url']
        return cls(name, types, base_stats, evs, moves, height, weight, image_url=image_url)

    def load_image(self):
        """Carga la imagen del Pokémon si está disponible en el directorio de imágenes."""
        image_path = f'assets/pokemon_images/{self.name.lower()}.png'
        if os.path.exists(image_path):
            return Image.open(image_path)
        return None  # Devuelve None si no se encuentra la imagen


def load_pokemon_data(file_path='data/pokemon_data.json'):
    """Cargar la lista de datos de Pokémon desde un archivo JSON."""
    with open(file_path, 'r') as file:
        return json.load(file)


def create_random_pokemon(pokemon_data_list):
    """Crear un Pokémon aleatorio a partir de una lista de datos de Pokémon."""
    random_pokemon_data = random.choice(pokemon_data_list)
    return Pokemon.from_json(random_pokemon_data)
