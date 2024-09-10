import pygame
import os


class TypeIcons:
    def __init__(self, icon_directory='../assets/img/types/', icon_size=(32, 32)):
        """
        Inicializa la clase TypeIcons.
        :param icon_directory: Directorio donde se encuentran las imágenes de los tipos.
        :param icon_size: Tamaño deseado para los iconos de los tipos.
        """
        self.icon_directory = icon_directory
        self.icon_size = icon_size
        self.type_to_icon = {
            'fire': 'fire.png',
            'water': 'water.png',
            'grass': 'grass.png',
            'electric': 'electric.png',
            'ice': 'ice.png',
            'fighting': 'fighting.png',
            'poison': 'poison.png',
            'ground': 'ground.png',
            'flying': 'flying.png',
            'psychic': 'psychic.png',
            'bug': 'bug.png',
            'rock': 'rock.png',
            'ghost': 'ghost.png',
            'dragon': 'dragon.png',
            'dark': 'dark.png',
            'steel': 'steel.png',
            'fairy': 'fairy.png',
            'normal': 'normal.png'
        }

        # Cargar las imágenes de los tipos al inicializar
        self.type_icons = self.load_icons()

    def load_icons(self):
        """Carga todas las imágenes de los tipos de Pokémon y las redimensiona al tamaño especificado."""
        icons = {}
        for pokemon_type, filename in self.type_to_icon.items():
            path = os.path.join(self.icon_directory, filename)
            if os.path.exists(path):
                # Cargar la imagen
                icon = pygame.image.load(path)
                # Redimensionar la imagen
                icon = pygame.transform.scale(icon, self.icon_size)
                icons[pokemon_type] = icon
            else:
                print(f"Imagen para el tipo '{pokemon_type}' no encontrada en {path}.")
        return icons

    def get_icon(self, pokemon_type):
        """Obtiene la imagen correspondiente al tipo de Pokémon."""
        return self.type_icons.get(pokemon_type, None)  # Devuelve None si no se encuentra el tipo
