import pygame
import os


def load_image(image_path, scale=None):
    """Cargar y escalar una imagen desde la ruta especificada."""
    image = pygame.image.load(os.path.abspath(image_path)).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image


def load_all_pokemon_images(directory="../assets/pokemon_images", scale=None):
    """Cargar todas las imágenes de los Pokemon y opcionalmente escalarlas."""
    images = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            image_name = os.path.splitext(filename)[0]
            images[image_name] = load_image(image_path, scale)
    return images


def load_font(font_path="../assets/fonts/pokemon.ttf"):
    """Cargar una fuente desde el archivo especificado, sin especificar el tamaño."""
    font_path = os.path.abspath(font_path)
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"No se encontró la fuente en la ruta: {font_path}")
    return font_path


def render_text(font_path, size, text, color):
    """Renderizar texto con el tamaño y color especificado."""
    font = pygame.font.Font(font_path, size)
    return font.render(text, True, color)


"""
Funciones para pintar y rendear las imágenes de los pokemon en combate.
"""


def draw_pokemon(screen, pokemon, position, scale_factor):
    """Dibuja un Pokémon en la pantalla en la posición dada con el tamaño escalado."""
    if pokemon.image:
        scaled_image = pygame.transform.scale(pokemon.image, (
            int(pokemon.image.get_width() * scale_factor),
            int(pokemon.image.get_height() * scale_factor)
        ))
        screen.blit(scaled_image, position)


def resize_image_to_width(image, new_width):
    """Redimensiona la imagen para que ajuste al nuevo ancho manteniendo las proporciones."""
    original_width, original_height = image.get_size()
    new_height = int((new_width / original_width) * original_height)
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    return resized_image
