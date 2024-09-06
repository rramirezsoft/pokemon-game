import pygame


def draw_dialog_box(screen, position, box_width=780, box_height=150, border_color=(0, 0, 0), border_thickness=5,
                    fill_color=(255, 255, 255), border_radius=20):
    """
    Dibuja un cuadro de diálogo estilizado.

    :param screen: La superficie en la que dibujar el cuadro de diálogo.
    :param position: Una tupla (x, y) que representa la posición del cuadro de diálogo.
    :param box_width: El ancho del cuadro de diálogo.
    :param box_height: La altura del cuadro de diálogo.
    :param border_color: Color del borde del cuadro de diálogo.
    :param border_thickness: Grosor del borde del cuadro de diálogo.
    :param fill_color: Color de fondo del cuadro de diálogo.
    :param border_radius: Radio de los bordes redondeados del cuadro de diálogo.
    """
    x, y = position

    # Crear una superficie temporal para el cuadro de diálogo con bordes redondeados
    dialog_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(dialog_surface, fill_color, (0, 0, box_width, box_height), border_radius=border_radius)
    pygame.draw.rect(dialog_surface, border_color, (0, 0, box_width, box_height), border_radius=border_radius,
                     width=border_thickness)

    # Blit del cuadro de diálogo en la superficie principal
    screen.blit(dialog_surface, (x, y))


def draw_text_in_dialog_box(screen, text, font, position, box_width=780, box_height=150,
                            text_color=(0, 0, 0), padding=20, line_spacing=10, vertical_offset=-15):
    """
    Dibuja el texto dentro del cuadro de diálogo.

    :param screen: La superficie en la que dibujar el texto.
    :param text: El texto que se va a dibujar.
    :param font: La fuente para el texto.
    :param position: Una tupla (x, y) que representa la posición del cuadro de diálogo.
    :param box_width: El ancho del cuadro de diálogo.
    :param box_height: La altura del cuadro de diálogo.
    :param text_color: Color del texto.
    :param padding: Espacio alrededor del texto dentro del cuadro de diálogo.
    :param line_spacing: Espacio adicional entre las líneas de texto.
    :param vertical_offset: Desplazamiento vertical adicional para el inicio del texto.
    """
    x, y = position

    # Dividir el texto en líneas si es necesario
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] > box_width - 2 * padding:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line)

    # Calcular el espacio disponible para el texto
    total_text_height = len(lines) * (font.get_height() + line_spacing) - line_spacing
    y_start = y + padding + (box_height - total_text_height) / 2 + vertical_offset

    # Dibujar el texto dentro del cuadro de diálogo
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect(topleft=(x + padding, y_start + i * (font.get_height() + line_spacing)))
        screen.blit(text_surface, text_rect)
