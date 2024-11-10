import pygame
import os


class IconLoader:
    def __init__(self, icon_directory, icon_size=(32, 32)):
        """
        Inicializa la clase IconLoader.
        :param icon_directory: Directorio donde se encuentran las imágenes.
        :param icon_size: Tamaño deseado para los iconos.
        """
        self.icon_directory = icon_directory
        self.icon_size = icon_size
        self.icons = {}

    def load_icons(self, icon_map):
        """Carga todas las imágenes y las redimensiona al tamaño especificado."""
        for key, filename in icon_map.items():
            path = os.path.join(self.icon_directory, filename)
            if os.path.exists(path):
                # Cargar la imagen
                icon = pygame.image.load(path)
                # Redimensionar la imagen
                icon = pygame.transform.scale(icon, self.icon_size)
                self.icons[key] = icon
            else:
                print(f"Imagen para '{key}' no encontrada en {path}.")

    def get_icon(self, key):
        """Obtiene la imagen correspondiente al tipo o género."""
        return self.icons.get(key, None)  # Devuelve None si no se encuentra el tipo o género


class TypeIcons(IconLoader):
    def __init__(self, icon_directory='../assets/img/types/', icon_size=(32, 32)):
        """
        Inicializa la clase TypeIcons.
        :param icon_directory: Directorio donde se encuentran las imágenes de los tipos.
        :param icon_size: Tamaño deseado para los iconos de los tipos.
        """
        super().__init__(icon_directory, icon_size)
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
        self.load_icons(self.type_to_icon)


class GenderIcons(IconLoader):
    def __init__(self, icon_directory='../assets/img/gender/', icon_size=(26, 26)):
        """
        Inicializa la clase GenderIcons.
        :param icon_directory: Directorio donde se encuentran las imágenes de los géneros.
        :param icon_size: Tamaño deseado para los iconos de los géneros.
        """
        super().__init__(icon_directory, icon_size)
        self.gender_to_icon = {
            'male': 'male.png',
            'female': 'female.png'
            # No se necesita un icono para 'N/A'
        }
        # Cargar las imágenes de los géneros al inicializar
        self.load_icons(self.gender_to_icon)
