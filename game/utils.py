import json

import pygame
import os
import ui


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


"""
Funciones para manejar las ventanas de confirmación (YES/NO)
"""


def handle_confirmation_navigation(selected_option, key):
    """Maneja la navegación entre las opciones de confirmación (Sí/No)."""
    if key in (pygame.K_UP, pygame.K_DOWN):
        return 'yes' if selected_option == 'no' else 'no'
    return selected_option


def draw_confirmation_box(screen, selected_option, position=(0, 0), box_width=140, box_height=140):
    """Dibuja la caja de confirmación de "Sí" o "No"."""
    confirmation_box_x, confirmation_box_y = position

    # Dibuja el cuadro de confirmación con el mismo estilo que la caja de diálogo
    ui.draw_dialog_box(screen, position=(confirmation_box_x, confirmation_box_y),
                       box_width=box_width, box_height=box_height)

    confirmation_font = pygame.font.Font(load_font(), 35)

    # Texto "Yes" y "No"
    yes_text = confirmation_font.render("Yes", True, (0, 0, 0))
    no_text = confirmation_font.render("No", True, (0, 0, 0))

    # Posiciones del texto "Yes" y "No"
    yes_text_pos = (confirmation_box_x + 50, confirmation_box_y + 25)
    no_text_pos = (confirmation_box_x + 50, confirmation_box_y + 75)

    screen.blit(yes_text, yes_text_pos)
    screen.blit(no_text, no_text_pos)

    # Dibuja la flecha ">" al lado de la opción seleccionada
    arrow_text = confirmation_font.render(">", True, (0, 0, 0))
    if selected_option == 'yes':
        screen.blit(arrow_text, (yes_text_pos[0] - 20, yes_text_pos[1]))
    else:
        screen.blit(arrow_text, (no_text_pos[0] - 20, no_text_pos[1]))


def load_pokemon_data(file_path='data/poke_data.json'):
    """Cargar la lista de datos de Pokémon desde un archivo JSON."""
    with open(file_path, 'r') as file:
        return json.load(file)
