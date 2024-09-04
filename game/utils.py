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


def load_font(font_path="../assets/fonts/PressStart2P-Regular.ttf"):
    """Cargar una fuente desde el archivo especificado, sin especificar el tamaño."""
    font_path = os.path.abspath(font_path)
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"No se encontró la fuente en la ruta: {font_path}")
    return font_path


def render_text(font_path, size, text, color):
    """Renderizar texto con el tamaño y color especificado."""
    font = pygame.font.Font(font_path, size)
    return font.render(text, True, color)
