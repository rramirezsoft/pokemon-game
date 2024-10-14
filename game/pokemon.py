import json
import random
import os
from PIL import Image
import pygame


class Pokemon:
    generated_ids = set()  # Set para almacenar todos los IDs generados

    def __init__(self, name, types, base_stats, evs, moves, height, weight, pokedex_id, random_id=None,
                 experience=0, level=None, ivs=None, status=None):
        self.name = name
        self.types = types
        self.base_stats = base_stats
        self.evs = evs
        self.ivs = ivs if ivs is not None else self.generate_ivs()
        self.level = random.randint(5, 100) if level is None else level
        self.moves = self.select_moves(moves)
        self.height = height / 10  # Conversión a metros
        self.weight = weight / 10  # Conversión a kilogramos
        self.experience = experience
        self.experience_to_next_level = self.calculate_exp_to_next_level()
        self.status = status
        self.image = self.load_image()  # Cargar la imagen al inicializar
        self.max_stats = self.calculate_stats()  # Guardar las estadísticas máximas
        self.current_stats = self.max_stats.copy()  # Inicializar los HP actuales al máximo
        self.current_hp = self.current_stats.get('hp', 0)  # Inicializar HP actuales
        self.random_id = random_id if random_id is not None else self.generate_random_id()  # ID de 6 cifras random
        self.pokedex_id = pokedex_id  # Almacenar el ID de la Pokédex

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

    @staticmethod
    def generate_random_id():
        """
        Genera un ID de 6 cifras unico para cada pokemon.
        Verifica que el ID no se repita
        """
        while True:
            new_id = random.randint(100000, 999999)
            if new_id not in Pokemon.generated_ids:
                Pokemon.generated_ids.add(new_id)
                return new_id

    def select_moves(self, moves):
        """Seleccionar hasta 4 movimientos disponibles según el nivel del Pokémon."""
        available_moves = [move for move in moves if move['level'] <= self.level]
        selected_moves = random.sample(available_moves, min(len(available_moves), 4))

        for move in selected_moves:
            move['current_pp'] = move['pp']  # Inicializa current_pp con los PP máximos

        return selected_moves

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

    def set_current_hp(self, hp):
        """Establece el HP actual del Pokémon."""
        self.current_hp = max(0, min(hp, self.max_stats.get('hp', 0)))

    def is_fainted(self):
        """Determina si el Pokémon está debilitado (faint)."""
        return self.current_hp <= 0

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
            "image": self.image,
        }

    @classmethod
    def from_json(cls, pokemon_data, level=None):
        """Crear un Pokémon a partir de los datos en formato JSON."""
        name = pokemon_data['name'].capitalize()
        types = pokemon_data['types']
        base_stats = {stat_name: stat_info['base_stat'] for stat_name, stat_info in pokemon_data['stats'].items()}
        evs = {stat_name: stat_info['evs'] for stat_name, stat_info in pokemon_data['stats'].items()}
        moves = pokemon_data['moves']
        height = pokemon_data['physical_attributes']['height']
        weight = pokemon_data['physical_attributes']['weight']
        pokedex_id = pokemon_data['id']

        return cls(name, types, base_stats, evs, moves, height, weight, pokedex_id, level=level)

    def load_image(self, desired_size=None):
        """Carga la imagen del Pokémon a su tamaño original y la redimensiona si es necesario."""
        image_path = f'../assets/pokemon_images/{self.name.lower()}.png'
        if os.path.exists(image_path):
            pil_image = Image.open(image_path)

            # Si se proporciona un tamaño deseado, redimensionar la imagen
            if desired_size:
                pil_image = self.resize_image(pil_image, desired_size)

            return self.pil_to_pygame(pil_image)
        return None  # Devuelve None si no se encuentra la imagen

    @staticmethod
    def pil_to_pygame(pil_image):
        """Convierte una imagen PIL a un objeto pygame.Surface."""
        pil_image = pil_image.convert("RGBA")
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()

        pygame_image = pygame.image.fromstring(data, size, mode)
        return pygame_image

    @staticmethod
    def resize_image(pil_image, size):
        """Redimensiona la imagen PIL a un tamaño específico."""
        return pil_image.resize(size, Image.Resampling.LANCZOS)


def load_pokemon_data(file_path='data/poke_data.json'):
    """Cargar la lista de datos de Pokémon desde un archivo JSON."""
    with open(file_path, 'r') as file:
        return json.load(file)


def create_random_pokemon(pokemon_data_list):
    """Crear un Pokémon aleatorio a partir de una lista de datos de Pokémon."""
    random_pokemon_data = random.choice(pokemon_data_list)
    return Pokemon.from_json(random_pokemon_data)


def create_pokemon(name, level=None):
    pokemon_data_list = load_pokemon_data()

    # Buscar el Pokémon por nombre
    for pokemon_data in pokemon_data_list:
        if pokemon_data['name'].lower() == name.lower():
            return Pokemon.from_json(pokemon_data, level=level)

    print(f"Pokémon con nombre '{name}' no encontrado.")
    return None
