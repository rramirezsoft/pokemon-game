import os

import pygame
import pygame.gfxdraw
import math
import game.utils as utils
from game.types import TypeIcons


def draw_gradient(screen, start_color, end_color, rect):
    """Dibuja un degradado vertical de `start_color` a `end_color` en el rectángulo."""
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    for i in range(rect.height):
        # Interpolar entre el color inicial y final
        ratio = i / rect.height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        pygame.draw.line(screen, (r, g, b), (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))


class Button:
    def __init__(self, text, rect, font, image=None, bg_color=(100, 149, 237),
                 text_color=(0, 0, 0), hover_color=(70, 130, 180),
                 border_color=(255, 255, 255), shadow_color=(50, 50, 50)):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.shadow_color = shadow_color
        self.image = image
        self.is_hovered = False

        if self.image:
            self.image = pygame.transform.scale(self.image, (50, 50))

    def draw(self, screen):
        """Dibuja el botón en pantalla con efectos avanzados."""
        # Cambiar el color de fondo si el ratón está sobre el botón
        current_color = self.hover_color if self.is_hovered else self.bg_color

        # Fondo con degradado avanzado para darle profundidad (de azul claro a más oscuro)
        draw_gradient(screen, current_color, (135, 206, 250), self.rect)

        # Bordes con brillo alrededor del botón
        pygame.gfxdraw.rectangle(screen, self.rect, self.border_color)

        # Dibujar sombra ligera para dar efecto 3D
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(3, 3)  # Desplazar la sombra ligeramente
        pygame.gfxdraw.box(screen, shadow_rect, (*self.shadow_color, 100))  # Sombra semi-transparente

        # Dibujar la imagen si está disponible
        if self.image:
            image_rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery - 20))  # Subir la imagen
            screen.blit(self.image, image_rect)

        # Dibujar el texto centrado debajo de la imagen
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 25))
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        """Detecta si el botón ha sido clicado."""
        return self.rect.collidepoint(mouse_pos)

    def update(self, mouse_pos):
        """Actualizar el estado hover según la posición del ratón."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)


def draw_combat_background(screen, position=(0, 449), width=800, height=151, color=(232, 210, 218), border=3):
    """
    Dibuja un recuadro de fondo para el menú de combate.

    :param screen: La superficie en la que dibujar el fondo.
    :param position: Una tupla (x, y) que representa la posición del fondo.
    :param width: Ancho del fondo.
    :param height: Altura del fondo.
    :param color: Color de relleno del fondo.
    :param border: Grosor del borde (en este caso, para la línea negra superior).
    """
    x, y = position

    # 1. Dibujar el fondo principal con el color de relleno
    pygame.draw.rect(screen, color, (x, y, width, height))

    # 2. Dibujar una línea gris en la parte superior del fondo (borde superior)
    pygame.draw.line(screen, (80, 80, 80), (x, y), (x + width, y), border)

    # 3. Dibujar una línea negra fina sobre la línea gris (parte superior) de 2 píxeles
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x + width, y), 2)


def draw_dialog_box(screen, position=(4, 456), box_width=792, box_height=140,
                    outer_border_color=(218, 165, 32),  # Dorado para el borde exterior
                    inner_border_color=(75, 77, 76),  # Grisáceo para el borde interior
                    border_thickness=2,  # Borde exterior fino negro
                    inner_border_thickness=4,  # Borde dorado más fino
                    side_inner_border_thickness=15,  # Grosor mayor a los lados del borde gris
                    top_bottom_inner_border_thickness=5,  # Grosor menor arriba y abajo del borde gris
                    fill_color=(255, 255, 255), outer_border_radius=5, inner_border_radius=3,
                    inner_fill_radius=2):
    """
    Dibuja un cuadro de diálogo estilizado al estilo Pokémon Platino con bordes dorados y grisáceos.

    :param screen: La superficie en la que dibujar el cuadro de diálogo.
    :param position: Una tupla (x, y) que representa la posición del cuadro de diálogo.
    :param box_width: El ancho del cuadro de diálogo.
    :param box_height: La altura del cuadro de diálogo.
    :param outer_border_color: Color del borde exterior (dorado).
    :param inner_border_color: Color del borde interior (grisáceo).
    :param border_thickness: Grosor del borde exterior (negro).
    :param inner_border_thickness: Grosor del borde dorado.
    :param side_inner_border_thickness: Grosor mayor en los lados del borde grisáceo.
    :param top_bottom_inner_border_thickness: Grosor menor arriba y abajo del borde grisáceo.
    :param fill_color: Color de fondo del cuadro de diálogo (blanco).
    :param outer_border_radius: Radio de los bordes redondeados del borde exterior.
    :param inner_border_radius: Radio de los bordes redondeados del borde interior.
    :param inner_fill_radius: Radio del borde de la caja interna (muy sutil).
    """
    x, y = position

    # Crear la superficie para el cuadro de diálogo
    dialog_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

    # Dibujar el borde negro exterior muy sutil
    pygame.draw.rect(dialog_surface, (0, 0, 0), (0, 0, box_width, box_height),
                     border_radius=outer_border_radius, width=border_thickness)

    # Dibujar el borde dorado justo dentro del negro
    pygame.draw.rect(dialog_surface, outer_border_color,
                     (border_thickness, border_thickness, box_width - 2 * border_thickness,
                      box_height - 2 * border_thickness),
                     border_radius=outer_border_radius, width=inner_border_thickness)

    # Dibujar el borde grisáceo interior (más grueso a los lados, más delgado arriba y abajo)
    inner_rect = pygame.Rect(
        border_thickness + inner_border_thickness,  # Empieza después del borde negro y dorado
        border_thickness + top_bottom_inner_border_thickness,  # Ajuste arriba
        box_width - 2 * (border_thickness + inner_border_thickness),  # Ajustar el ancho
        box_height - 2 * top_bottom_inner_border_thickness - 4
    )
    pygame.draw.rect(dialog_surface, inner_border_color, inner_rect,
                     border_radius=inner_border_radius, width=side_inner_border_thickness)

    # Dibujar el relleno blanco dentro del cuadro de diálogo (casi sin radius)
    fill_rect = pygame.Rect(
        border_thickness + inner_border_thickness + side_inner_border_thickness,  # Ajuste en los lados
        border_thickness + top_bottom_inner_border_thickness + inner_border_thickness,  # Ajuste arriba
        box_width - 2 * (border_thickness + inner_border_thickness + side_inner_border_thickness),  # Ajustar el ancho
        box_height - 2 * (top_bottom_inner_border_thickness + inner_border_thickness + 3)
    )
    pygame.draw.rect(dialog_surface, fill_color, fill_rect, border_radius=inner_fill_radius)

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


class HealthBar:
    def __init__(self, max_hp, current_hp, rect,
                 text_color=(0, 0, 0), font_size=20, bar_color=(0, 255, 0),
                 background_color=(169, 169, 169), selected=False):
        """
        :param max_hp: HP máximo del Pokémon.
        :param current_hp: HP actual del Pokémon.
        :param rect: La posición y tamaño de la barra (x, y, width, height).
        :param text_color: Color del texto que muestra el HP.
        :param font_size: Tamaño de la fuente para el texto de HP.
        :param bar_color: Color de la barra de salud.
        :param background_color: Color del fondo de la barra cuando está vacía.
        :param selected: Indica si el slot está seleccionado.
        """
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.target_hp = current_hp  # Para la animación suave
        self.rect = pygame.Rect(rect)
        self.text_color = text_color
        self.font = pygame.font.Font('../assets/fonts/pokemon.ttf', font_size)
        self.bar_color = bar_color
        self.background_color = background_color
        self.selected = selected

    def update(self, current_hp):
        """
        Actualiza la barra de vida de manera progresiva.

        :param current_hp: El nuevo HP del Pokémon.
        """
        self.target_hp = current_hp

    def get_health_percentage(self):
        """Retorna el porcentaje de vida restante."""
        return self.current_hp / self.max_hp

    def smooth_transition(self):
        """Transición suave del HP actual hacia el HP objetivo."""
        if self.current_hp < self.target_hp:
            self.current_hp += 1  # Aumenta suavemente
        elif self.current_hp > self.target_hp:
            self.current_hp -= 1  # Disminuye suavemente

    def draw(self, screen):
        """Dibuja la barra de vida con todos los detalles estéticos."""
        # Transición suave del HP
        self.smooth_transition()

        # Calcula el porcentaje de vida
        health_percentage = self.get_health_percentage()

        # Determina el color de la barra según el porcentaje
        if health_percentage > 0.5:
            color = self.bar_color  # Verde
        elif 0.25 < health_percentage <= 0.5:
            color = (255, 255, 0)  # Amarillo
        elif 0.1 < health_percentage <= 0.25:
            color = (255, 165, 0)  # Naranja
        else:
            color = (255, 0, 0)  # Rojo

        # Dibuja el fondo de la barra (cuando está vacía)
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=3)

        # Calcula el ancho de la barra según el porcentaje de vida restante
        health_width = int(self.rect.width * health_percentage)

        # Crea un rectángulo para la barra interna (vida restante)
        inner_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)

        # Dibuja la barra interna (con esquinas redondeadas)
        pygame.draw.rect(screen, color, inner_rect, border_radius=3)

        # Cambiar el color del texto si está seleccionado
        hp_text_color = (255, 255, 255) if self.selected else self.text_color

        # Dibuja texto de HP debajo de la barra
        hp_text = f"{self.current_hp}/{self.max_hp}"
        text_surface = self.font.render(hp_text, True, hp_text_color)
        text_rect = text_surface.get_rect(midtop=(self.rect.x + 25, self.rect.bottom + 3))  # Justo debajo de la barra
        screen.blit(text_surface, text_rect)


class PokemonSlot:
    def __init__(self, pokemon, rect, selected=False):
        """
        Inicializa el slot de un Pokémon.

        :param pokemon: Objeto Pokémon que contiene la información del Pokémon.
        :param rect: pygame.Rect que contiene la posición (x, y) y tamaño (ancho, alto) de la caja.
        :param selected: Indica si el slot está seleccionado.
        """
        self.pokemon = pokemon  # El Pokémon asignado a este slot.
        self.rect = pygame.Rect(rect)  # El rectángulo que representa la posición y tamaño de la caja.
        self.selected = selected  # Estado de selección

        # Fuente para el texto
        self.font = pygame.font.Font('../assets/fonts/pokemon.ttf', 24)
        self.level_font = pygame.font.Font('../assets/fonts/pokemon.ttf', 20)

        # Inicializar la barra de salud si el Pokémon existe
        if pokemon:
            health_bar_rect = pygame.Rect(
                self.rect.x + self.rect.width * 0.20,  # Centrada en la caja
                self.rect.y + self.rect.height * 0.5,
                self.rect.width * 0.6,  # Ocupa el 60% del ancho de la caja
                self.rect.height * 0.1  # Ocupa el 9% de la altura de la caja
            )
            self.health_bar = HealthBar(
                pokemon.max_stats['hp'],
                pokemon.current_hp,
                health_bar_rect,
                selected=self.selected  # Pasar el estado de selección a HealthBar
            )

    def draw(self, screen):
        """
        Dibuja el slot del Pokémon en la pantalla.

        :param screen: Superficie de pygame en la que se dibuja.
        """
        # Cambiar color de fondo y texto dependiendo de la selección y estado del Pokémon
        if self.selected:
            bg_color = (0, 0, 0)
            text_color = (255, 255, 255)
        elif self.pokemon and self.pokemon.is_fainted():
            bg_color = (255, 0, 0)  # Rojo para Pokémon debilitado
            text_color = (255, 255, 255)
        else:
            bg_color = (255, 255, 255)
            text_color = (0, 0, 0)

        # Dibujar la caja con bordes redondeados
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=40)

        if self.pokemon:
            # Dibujar la imagen del Pokémon
            if self.pokemon.image:
                pokemon_image = pygame.transform.scale(self.pokemon.image,
                                                       (self.rect.height * 0.6, self.rect.height * 0.6))
                screen.blit(pokemon_image, (self.rect.x + 10, self.rect.y + self.rect.height * 0.2))

            # Actualizar el color del texto en la barra de salud
            self.health_bar.selected = self.selected
            # Dibujar la barra de salud
            self.health_bar.draw(screen)

            # Dibujar el nombre del Pokémon
            name_text = self.font.render(self.pokemon.name, True, text_color)
            screen.blit(name_text, (self.rect.x + self.rect.width * 0.20, self.rect.y + self.rect.height * 0.1))

            # Dibujar el nivel del Pokémon
            level_text = self.level_font.render(f"Nv. {self.pokemon.level}", True, text_color)
            screen.blit(level_text, (self.rect.x + self.rect.width * 0.75, self.rect.y + self.rect.height * 0.6))
        else:
            # Si no hay Pokémon, dibujar un placeholder o simplemente dejarlo vacío
            placeholder_text = self.font.render("Empty Slot", True, (150, 150, 150))
            screen.blit(placeholder_text, self.rect.move(10, 10))


class Footer:
    def __init__(self, text, screen_width=800, icon_path="../assets/img/icons/atras.png",
                 font_path="../assets/fonts/pokemon.ttf", font_size=21):
        """
        Inicializa el footer con el icono y el texto.

        :param text: Texto a mostrar junto al icono.
        :param screen_width: Ancho de la pantalla para centrar el icono y el texto.
        :param icon_path: Ruta al archivo del icono.
        :param font_path: Ruta al archivo de la fuente.
        :param font_size: Tamaño de la fuente.
        """
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (20, 20))  # Ajustar el tamaño del icono
        self.text = text
        self.font = pygame.font.Font(font_path, font_size)
        self.footer_height = 25
        self.screen_width = screen_width
        self.footer_rect = pygame.Rect(0, 0, screen_width, self.footer_height)
        self.text_rect = pygame.Rect(0, 0, 0, 0)
        self.update_text_position()

    def update_text_position(self):
        """
        Actualiza la posición del texto basado en la posición del icono.
        """
        icon_x = self.screen_width - 100
        icon_y = (self.footer_height - self.icon.get_height()) // 2
        self.text_rect = self.font.render(self.text, True, (255, 255, 255)).get_rect(
            midleft=(icon_x + 30, self.footer_rect.centery))

    def draw(self, screen):
        """
        Dibuja el footer en la pantalla.

        :param screen: Superficie de pygame en la que se dibuja.
        """
        # Ajusta la posición del footer en la parte inferior de la pantalla
        self.footer_rect.bottomleft = (0, screen.get_height())

        # Dibuja el fondo del footer
        pygame.draw.rect(screen, (20, 20, 20), self.footer_rect)  # Casi negro

        # Dibuja el icono
        icon_x = self.footer_rect.width - 100
        icon_y = self.footer_rect.y + (self.footer_height - self.icon.get_height()) // 2
        screen.blit(self.icon, (icon_x, icon_y))

        # Dibuja el texto
        self.update_text_position()
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Texto en blanco
        screen.blit(text_surface, self.text_rect)

    def handle_events(self, event):
        """
        Maneja eventos, como clics del ratón sobre el footer.

        :param event: Evento de pygame.
        :return: `True` si se hace clic en el área del texto, `False` en caso contrario.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.text_rect.collidepoint(mouse_pos):
                return True
        return False


class MiniMenu:
    def __init__(self, position, size=(150, 120), font_path="../assets/fonts/pokemon.ttf", font_size=22, options=None):
        self.position = position
        self.width, self.height = size
        self.background_color = (255, 255, 255)  # Blanco
        self.font_color = (0, 0, 0)  # Negro
        self.font_size = font_size
        self.font = pygame.font.Font(font_path, font_size)
        self.options = options if options else ["Data", "Move", "Back"]
        self.border_radius = 10
        self.show = False
        self.selected_index = 0  # Índice de la opción seleccionada

        # Crear el rectángulo del menú
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

    def draw(self, screen):
        if not self.show:
            return

        # Crear una superficie para la sombra con un gradiente
        shadow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, 80)  # Negro con opacidad
        pygame.draw.rect(shadow_surface, shadow_color, (0, 0, self.width, self.height),
                         border_radius=self.border_radius)

        # Dibujar la sombra en la superficie del menú
        shadow_rect = self.rect.move(3, 3)  # Mueve la sombra ligeramente hacia abajo y a la derecha
        screen.blit(shadow_surface, shadow_rect)

        # Dibujar el fondo del mini menú con bordes redondeados
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=self.border_radius)

        # Dibujar un borde más acentuado
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=self.border_radius)

        # Dibujar el texto en el mini menú con flecha para la opción seleccionada
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, self.font_color)
            text_rect = text_surface.get_rect(
                topleft=(self.position[0] + 30, self.position[1] + 10 + i * (self.font_size + 5)))

            # Dibuja el texto
            screen.blit(text_surface, text_rect)

            # Dibuja la flecha `>` al lado de la opción seleccionada
            if i == self.selected_index:  # Ajusta el índice según la opción preseleccionada
                arrow_surface = self.font.render('>', True, self.font_color)
                arrow_rect = arrow_surface.get_rect(
                    topleft=(self.position[0] + 10, self.position[1] + 10 + i * (self.font_size + 5)))
                screen.blit(arrow_surface, arrow_rect)

    def toggle(self):
        """Alterna la visibilidad del mini menú."""
        self.show = not self.show

    def is_mouse_over(self, mouse_pos):
        """Verifica si el ratón está sobre el mini menú."""
        return self.rect.collidepoint(mouse_pos)

    def is_option_clicked(self, mouse_pos):
        """ Verifica si se ha hecho clic en una de las opciones del mini menú. """
        for i, option in enumerate(self.options):
            # Obtener la posición y tamaño de la opción
            text_surface = self.font.render(option, True, self.font_color)
            text_rect = text_surface.get_rect(topleft=(self.position[0] + 10,
                                                       self.position[1] + 10 + i * (self.font_size + 5)))
            if text_rect.collidepoint(mouse_pos):
                return i  # Retorna el índice de la opción clickeada
        return None  # No se hizo clic en ninguna opción


def draw_pokemon_background(screen, triangle_points, stripe_points, img_position, img_size,
                            img_path="../assets/img/pokemon_menu/info.png", angle_rotation=15,
                            background_color=(233, 239, 255), triangle_color=(227, 49, 63), stripe_color=(196, 40, 53)):
    """
    Dibuja un fondo para el menú de equipo Pokémon.

    :param screen: Superficie de pygame en la que se dibuja el fondo.
    :param triangle_points: Lista de puntos (x, y) para el triángulo rojo.
    :param stripe_points: Lista de puntos (x, y) para la franja diagonal en rojo oscuro.
    :param img_position: Tupla (x, y) para la posición de la Pokéball.
    :param img_size: Tamaño de la pokeball
    :param img_path: Ruta de la imagen de fondo.
    :param angle_rotation: Ángulo de rotación de la imagen.
    :param background_color: Color de fondo.
    :param triangle_color: Color del triángulo.
    :param stripe_color: Color de la franja diagonal
    """

    # Obtener el tamaño de la pantalla
    screen.fill(background_color)

    # Dibujar el triángulo rojo brillante
    pygame.draw.polygon(screen, triangle_color, triangle_points)

    # Dibujar la franja diagonal en rojo oscuro que sea paralela al triángulo
    pygame.draw.polygon(screen, stripe_color, stripe_points)

    # Dibujar la pokeball de fondo.
    image = pygame.image.load(img_path)

    # Escalar la imagen de la Pokéball a 600px
    img_scaled = pygame.transform.scale(image, img_size)

    # Girar la imagen de la Pokéball un poco (por ejemplo, 15 grados)
    img_rotated = pygame.transform.rotate(img_scaled, angle_rotation)

    # Obtener el rectángulo de la imagen rotada para centrarla correctamente
    img_rect = img_rotated.get_rect()
    img_rect.topleft = img_position

    # Dibujar la imagen de la Pokéball
    screen.blit(img_rotated, img_rect.topleft)


def draw_interactive_arrow(screen, coords, color, action=None):
    """
    Dibuja un triángulo interactivo en la pantalla y ejecuta una acción si se hace clic en él.

    :param screen: La pantalla en la que se va a dibujar.
    :param coords: Coordenadas del triángulo (una lista de tres tuplas).
    :param color: El color del triángulo.
    :param action: Función que se ejecuta cuando se hace clic en el triángulo.
    """
    # Dibuja el triángulo
    pygame.draw.polygon(screen, color, coords)

    # Define el área rectangular que envuelve el triángulo
    min_x = min([x for x, y in coords])
    min_y = min([y for x, y in coords])
    max_x = max([x for x, y in coords])
    max_y = max([y for x, y in coords])
    arrow_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    # Devolvemos el rectángulo para usarlo en la detección de clics
    return arrow_rect


def draw_interactive_icon(screen, image_path, image_size, coords, action=None):
    """
        Pinta un icono interactivo para ver estadisticas, movimientos, info...

        :param screen: La pantalla en la que se va a dibujar.
        :param image_path: Ruta del icono.
        :param image_size: Tamaño de la imagen
        :param coords: Coordenadas del icono (una lista de tres tuplas).
        :param action: Función que se ejecuta cuando se hace clic en el icono.
        """

    icon = pygame.image.load(image_path)
    icon = pygame.transform.scale(icon, image_size)

    screen.blit(icon, coords, action)


def draw_info_tab(screen, rect, font_size, pokemon, player):
    """
    :param screen: La pantalla en la que se va a dibujar.
    :param rect: El rectángulo en el que se dibujará el recuadro.
    :param font_size: Tamaño de la fuente del texto.
    :param pokemon: Objeto Pokémon que contiene la información a mostrar.
    :param player: Objeto Player para mostrar el nombre del entrenador del pokemon.
    """
    light_gray = (230, 230, 230)
    dark_gray = (200, 200, 200)
    text_color = (0, 0, 0)

    # Dimensiones del recuadro
    x, y, width, height = rect

    # Sombra en el lado derecho y abajo
    shadow_color = (100, 100, 100, 30)  # Color sombra con transparencia
    shadow_offset = 4  # Desplazamiento de la sombra

    # Crear una superficie con canal alfa para la sombra
    shadow_surface = pygame.Surface((width + shadow_offset, height + shadow_offset), pygame.SRCALPHA)

    # Dibujar la sombra (rectángulo desplazado)
    pygame.draw.rect(shadow_surface, shadow_color, (shadow_offset, shadow_offset, width, height))

    # Dibujar la sombra en la pantalla
    screen.blit(shadow_surface, (x, y))

    pygame.draw.rect(screen, (255, 255, 255), rect)

    x, y, width, height = rect

    # Dibuja la mitad izquierda del recuadro en gris claro
    pygame.draw.rect(screen, light_gray, (x, y, width // 2, height))

    # Dibuja las líneas grises horizontales sobre el recuadro
    section_height = height / 6
    for i in range(1, 6):
        pygame.draw.line(screen, dark_gray, (x, y + i * section_height), (x + width, y + i * section_height), 2)

    font = pygame.font.Font("../assets/fonts/pokemon.ttf", font_size)

    # Contenido de las celdas
    labels = [
        "Name",
        "Type",
        "Trainer",
        "ID No.",
        "Current no. of Exp. Points",
        "Points needed to level up"
    ]

    # Renderizar el texto en la mitad izquierda del recuadro
    for i, label in enumerate(labels):
        text_surface = font.render(label, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x + width // 4  # Centro horizontalmente en la mitad izquierda
        text_rect.centery = y + (i + 0.5) * section_height  # Centro verticalmente en la sección correspondiente
        screen.blit(text_surface, text_rect)

    # Renderizar el contenido en la mitad derecha del recuadro
    data = [
        pokemon.name,
        pokemon.types,  # Esto es para las imágenes de tipos
        player.name,
        pokemon.id,  # Para el ID No. puedes añadir un valor si lo tienes
        pokemon.experience,
        pokemon.experience_to_next_level
    ]

    icon_manager = TypeIcons(icon_size=(75, 30))
    for i, info in enumerate(data):
        if i == 1:  # Para el tipo del Pokémon
            # Mostrar imágenes en lugar de texto para el tipo
            types = pokemon.types

            # Calcula la posición inicial para dibujar las imágenes
            icon_x = x + width // 2 + 10
            icon_y = y + (i + 0.5) * section_height - 16  # Ajusta según el tamaño de tus imágenes

            for pokemon_type in types:
                icon = icon_manager.get_icon(pokemon_type)
                if icon:
                    screen.blit(icon, (icon_x, icon_y))
                    icon_x += icon.get_width() + 5  # Espacio entre iconos
        else:
            text_surface = font.render(str(info), True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.left = x + width // 2 + 10  # Posición desde el borde izquierdo de la mitad derecha
            text_rect.centery = y + (i + 0.5) * section_height  # Centro verticalmente en la sección correspondiente
            screen.blit(text_surface, text_rect)


def draw_stats_tb(screen, rect, font_size, pokemon):
    """
    Dibuja una gráfica hexagonal de las estadísticas del Pokémon.

    :param screen: La pantalla en la que se va a dibujar.
    :param rect: El rectángulo en el que se dibujará el gráfico.
    :param font_size: Tamaño de la fuente del texto.
    :param pokemon: Objeto Pokémon que contiene las estadísticas.
    """

    # Colores
    base_color = (200, 200, 200)
    stat_color = (0, 0, 255)
    text_color = (0, 0, 0)

    # Dimensiones del recuadro
    x, y, width, height = rect

    # Sombra en el lado derecho y abajo
    shadow_color = (100, 100, 100, 30)  # Color sombra con transparencia
    shadow_offset = 4  # Desplazamiento de la sombra

    # Crear una superficie con canal alfa para la sombra
    shadow_surface = pygame.Surface((width + shadow_offset, height + shadow_offset), pygame.SRCALPHA)

    # Dibujar la sombra (rectángulo desplazado)
    pygame.draw.rect(shadow_surface, shadow_color, (shadow_offset, shadow_offset, width, height))

    # Dibujar la sombra en la pantalla
    screen.blit(shadow_surface, (x, y))

    pygame.draw.rect(screen, (255, 255, 255), rect)

    # Coordenadas y dimensiones del rectángulo
    x, y, width, height = rect

    # Centro del hexágono
    center_x = x + width // 2
    center_y = y + height // 2
    radius = min(width, height) // 3  # Radio del hexágono

    # Estadísticas del Pokémon
    stats = {
        "HP": pokemon.current_stats["hp"],
        "Attack": pokemon.current_stats["attack"],
        "Defense": pokemon.current_stats["defense"],
        "Speed": pokemon.current_stats["speed"],
        "Sp. Defense": pokemon.current_stats["special-defense"],
        "Sp. Attack": pokemon.current_stats["special-attack"]
    }

    max_stat = 400  # Valor máximo de cada estadística

    # Nombres de las estadísticas
    stat_labels = list(stats.keys())

    # Calcular las posiciones de los vértices del hexágono base
    def get_vertex_positions(center_x, center_y, radius, offset=0):
        positions = []
        for i in range(6):
            angle_deg = 60 * i - 90 + offset  # Rotamos 90 grados para que el vértice superior sea HP
            angle_rad = math.radians(angle_deg)
            vertex_x = center_x + radius * math.cos(angle_rad)
            vertex_y = center_y + radius * math.sin(angle_rad)
            positions.append((vertex_x, vertex_y))
        return positions

    # Dibujar el hexágono base (grisáceo) - Representa el máximo de las estadísticas
    base_vertices = get_vertex_positions(center_x, center_y, radius)
    pygame.draw.polygon(screen, base_color, base_vertices, 3)  # Grosor 3 para el borde

    # Dibujar el hexágono de estadísticas (azul)
    stat_vertices = []
    for i, (stat, value) in enumerate(stats.items()):
        ratio = value / max_stat  # Proporción respecto al valor máximo
        stat_vertices.append((
            center_x + radius * ratio * math.cos(math.radians(60 * i - 90)),
            center_y + radius * ratio * math.sin(math.radians(60 * i - 90))
        ))
    pygame.draw.polygon(screen, stat_color, stat_vertices, 0)  # Sin borde, relleno

    # Dibujar líneas que separan los segmentos del hexágono
    for vertex in base_vertices:
        pygame.draw.line(screen, base_color, (center_x, center_y), vertex, 2)

    # Renderizar el texto de las estadísticas en los vértices (alejarlo ligeramente)
    font = pygame.font.Font("../assets/fonts/pokemon.ttf", font_size)
    label_offset = 30  # Distancia a la que se moverán las etiquetas de los vértices
    value_offset = 20  # Ajusta esto para controlar la separación entre el nombre y el valor

    for i, (label, vertex) in enumerate(zip(stat_labels, base_vertices)):
        # Mover el texto de la estadística un poco hacia afuera
        angle_deg = 60 * i - 90  # Ángulo de cada vértice
        angle_rad = math.radians(angle_deg)

        # Posicionar el nombre de la estadística
        label_x = vertex[0] + label_offset * math.cos(angle_rad)
        label_y = vertex[1] + label_offset * math.sin(angle_rad)

        # Dibujar el nombre de la estadística
        text_surface = font.render(label, True, text_color)
        text_rect = text_surface.get_rect(center=(label_x, label_y))
        # Calcular la posición del valor de la estadística
        value_x = label_x
        if i >= 3:
            value_y = label_y - value_offset
        else:
            value_y = label_y + value_offset

        # Dibujar el nombre de la estadística en la posición calculada
        screen.blit(text_surface, text_rect)

        # Dibujar el valor de la estadística debajo del nombre
        stat_value_surface = font.render(str(stats[label]), True, text_color)
        stat_value_rect = stat_value_surface.get_rect(center=(value_x, value_y))
        screen.blit(stat_value_surface, stat_value_rect)


def draw_moves_tab(screen, pokemon, position, font_size, selected_move_index=None,
                   box_color=(255, 255, 255), text_color=(0, 0, 0), gray_color=(84, 84, 84), selected_color=(0, 0, 0)):
    """
    Dibuja la pestaña de movimientos del Pokémon en la pantalla.

    :param screen: La superficie en la que dibujar.
    :param pokemon: El objeto Pokémon que contiene los movimientos.
    :param position: La posición en la pantalla donde empezar a dibujar.
    :param font_size: Tamaño de la fuente para el texto de los movimientos.
    :param selected_move_index: El índice del movimiento seleccionado (si lo hay).
    :param box_color: Color de fondo de las cajas de movimientos.
    :param text_color: Color del texto.
    :param gray_color: Color de la sección gris en la parte derecha de la caja.
    :param selected_color: Color de fondo para el movimiento seleccionado.
    :return: Una lista de rectángulos de los movimientos para la detección de clics.
    """
    box_width, box_height = 400, 50
    padding = 4
    gray_section_width = 80
    border_radius = 40
    x, y = position

    moves = pokemon.moves
    move_rects = []

    # Cargar los iconos de tipos de movimientos
    icon_manager = TypeIcons(icon_size=(75, 30))  # Asegúrate de que el tamaño sea el adecuado

    for i, move in enumerate(moves):
        # Usa el color de selección si el movimiento está seleccionado, de lo contrario, usa el color por defecto.
        current_box_color = selected_color if i == selected_move_index else box_color
        current_text_color = (255, 255, 255) if i == selected_move_index else text_color  # Blanco si está seleccionado

        # Dibuja el rectángulo del movimiento con el color correspondiente
        box_rect = pygame.Rect(x, y + i * (box_height + padding), box_width, box_height)
        gray_section_rect = pygame.Rect(box_rect.right - gray_section_width, box_rect.top, gray_section_width,
                                        box_height)

        # Dibuja los rectángulos
        pygame.draw.rect(screen, current_box_color, box_rect, border_radius=border_radius)
        pygame.draw.rect(screen, gray_color, gray_section_rect, border_radius=border_radius)

        # Dibuja el pequeño polígono gris en la sección gris
        small_polygon_width = gray_section_width * 0.6
        small_polygon_height = box_height
        offset = 20
        top_left = (
            gray_section_rect.left + (gray_section_width - small_polygon_width) / 2 - offset, gray_section_rect.top)
        top_right = (top_left[0] + small_polygon_width - 10, top_left[1])
        bottom_right = (top_left[0] + small_polygon_width - 10, gray_section_rect.bottom)
        bottom_left = (top_left[0] - gray_section_width * 0.3 + 4, gray_section_rect.bottom)
        small_polygon_points = [top_left, top_right, bottom_right, bottom_left]
        pygame.draw.polygon(screen, gray_color, small_polygon_points)

        # Renderiza el nombre del movimiento
        font = pygame.font.Font("../assets/fonts/pokemon.ttf", font_size)
        move_text = move['name']
        pp_text = "{}/{}".format(move['pp'], move['current_pp'])
        text_surface = font.render(move_text, True, current_text_color)
        pp_surface = font.render(pp_text, True, (255, 255, 255))

        text_rect = text_surface.get_rect(topleft=(box_rect.left + 10, box_rect.top
                                                   + (box_height - text_surface.get_height()) // 2))

        pp_rect = pp_surface.get_rect(topright=(box_rect.right - 25, box_rect.top
                                                + (box_height - pp_surface.get_height()) // 2))

        # Agregar icono del tipo de movimiento
        type_icon = icon_manager.get_icon(move['type'])  # Asegúrate de que 'type' esté en 'move'
        if type_icon:
            icon_rect = pygame.Rect(box_rect.width // 2 + 35, box_rect.top + (box_height - type_icon.get_height()) // 2,
                                    type_icon.get_width(), type_icon.get_height())
            screen.blit(type_icon, icon_rect)

        screen.blit(text_surface, text_rect)
        screen.blit(pp_surface, pp_rect)
        move_rects.append(box_rect)

    return move_rects


def draw_rectangles(screen, start_x, start_y, rect_width, rect_height, padding, border_radius, rect_color, font_size,
                    text_values=None, left_half_color=(220, 220, 220)):
    """
    Dibuja un conjunto de rectángulos con un borde redondeado en la pantalla.

    :param screen: La superficie en la que dibujar.
    :param start_x: La posición X inicial para el primer rectángulo.
    :param start_y: La posición Y inicial para el primer rectángulo.
    :param rect_width: El ancho de cada rectángulo.
    :param rect_height: La altura de cada rectángulo.
    :param padding: El espacio entre los rectángulos.
    :param border_radius: El radio de redondeo de las esquinas.
    :param rect_color: El color de fondo de los rectángulos.
    :param text_values: Un diccionario con los valores de texto a mostrar dentro de los rectángulos.
    :param font_size: Tamaño de la fuente a utilizar para el texto.
    :param left_half_color: Color de la mitad izquierda del recuadro.

    """
    current_y = start_y

    for i in range(len(text_values)):
        # Calcular la posición y el tamaño del rectángulo
        rect = pygame.Rect(start_x, current_y, rect_width, rect_height)

        # Dibujar el rectángulo completo blanco
        pygame.draw.rect(screen, rect_color, rect, border_radius=border_radius)

        # Dibujar la mitad izquierda del rectángulo color grisáceo
        half_rect = pygame.Rect(start_x, current_y, rect_width // 2, rect_height)
        pygame.draw.rect(screen, left_half_color, half_rect, border_radius=border_radius)

        # Avanzar la posición Y para el siguiente rectángulo
        current_y += rect_height + padding

    # Dibujar el texto en los rectángulos
    font = pygame.font.Font("../assets/fonts/pokemon.ttf", font_size)
    if text_values:
        draw_text_in_rect(screen, (start_x, start_y), (rect_height + padding), text_values, font, rect_width)


def draw_text_in_rect(screen, position, line_height, text_values, font, rect_width):
    """
    Dibuja el label en la parte izquierda y el valor en la parte derecha del rectángulo.

    :param screen: La superficie en la que dibujar.
    :param position: La posición (x, y) en la pantalla donde empezar a dibujar el texto.
    :param line_height: Espaciado entre líneas.
    :param text_values: Un diccionario con los valores de texto a mostrar.
    :param font: La fuente a utilizar para el texto.
    :param rect_width: El ancho del rectángulo, para saber dónde dividir la mitad.
    """
    if not isinstance(text_values, dict):
        raise TypeError("Expected text_values to be a dictionary, got {}".format(type(text_values)))

    for j, (label, value) in enumerate(text_values.items()):
        # Preparar el texto para el label (mitad izquierda, parte gris)
        label_surface = font.render(f"{label}", True, (0, 0, 0))
        label_rect = label_surface.get_rect(
            center=(position[0] + rect_width // 4, position[1] + j * line_height + line_height // 2)
        )

        # Preparar el texto para el value (mitad derecha, parte blanca)
        value_surface = font.render(f"{value}", True, (0, 0, 0))
        value_rect = value_surface.get_rect(
            center=(position[0] + 3 * rect_width // 4, position[1] + j * line_height + line_height // 2)
        )

        # Dibujar el label en la mitad izquierda (gris)
        screen.blit(label_surface, label_rect)

        # Dibujar el value en la mitad derecha (blanco)
        screen.blit(value_surface, value_rect)


def draw_description(screen, description, start_x, start_y, rect_width, rect_height, font_size, padding=10):
    """
    Dibuja una caja de descripción.

    :param screen: La superficie en la que dibujar.
    :param description: El texto de la descripción del movimiento.
    :param start_x: La posición X inicial para el rectángulo.
    :param start_y: La posición Y inicial para el rectángulo.
    :param rect_width: El ancho del rectángulo.
    :param rect_height: La altura del rectángulo.
    :param font_size: Tamaño de la fuente para el texto.
    :param padding: El espacio entre el rectángulo y el texto.
    """
    # Dibuja el rectángulo blanco para la descripción
    rect = pygame.Rect(start_x, start_y, rect_width, rect_height)
    pygame.draw.rect(screen, (255, 255, 255), rect)

    # Crear la fuente para el texto
    font = pygame.font.Font("../assets/fonts/pokemon.ttf", font_size)

    # Ajustar el texto
    wrapped_text = wrap_text(description, font, rect_width - 2 * padding)
    line_height = font.size("Tg")[1]

    # Calcular la altura total del texto para centrarlo
    total_text_height = len(wrapped_text) * line_height
    text_y = start_y + (rect_height - total_text_height) // 2

    # Dibujar cada línea de texto centrada horizontalmente
    for i, line in enumerate(wrapped_text):
        line_surface = font.render(line, True, (0, 0, 0))

        # Calcular posición centrada horizontalmente para cada línea
        text_x = start_x + (rect_width - line_surface.get_width()) // 2
        line_rect = line_surface.get_rect(topleft=(text_x, text_y + i * line_height))
        screen.blit(line_surface, line_rect)


def wrap_text(text, font, max_width):
    """
    Ajusta el texto para que quepa dentro del ancho máximo especificado.

    :param text: El texto a ajustar.
    :param font: La fuente utilizada para medir el texto.
    :param max_width: El ancho máximo en el que el texto debe caber.
    :return: Una lista de líneas de texto ajustadas.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


def start_battle_transition(player, enemy_pokemon):
    """Realiza la animación de transición de combate y luego inicia la batalla."""
    pokeball_image = utils.load_image("../assets/img/icons/pokeball.png")

    # Configuración inicial de la animación
    initial_size = 40
    final_size = max(pygame.display.get_surface().get_width(),
                     pygame.display.get_surface().get_height()) * 1.8
    rotation_angle = 0
    size = initial_size
    transition_complete = False

    screen = pygame.display.get_surface()

    # Ciclo para la animación
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not transition_complete:
            # Incrementar el tamaño de la Pokéball
            size_increment = 15
            size += size_increment
            if size >= final_size:
                size = final_size
                transition_complete = True

            # Actualizar el ángulo de rotación
            rotation_angle += 4
            if rotation_angle >= 360:
                rotation_angle -= 360

            # Dibujar la Pokébola escalada y rotada
            pokeball_scaled = pygame.transform.scale(pokeball_image, (size, size))
            pokeball_rotated = pygame.transform.rotate(pokeball_scaled, rotation_angle)

            # Centrar la imagen en la pantalla
            x = (pygame.display.get_surface().get_width() - size) // 2
            y = (pygame.display.get_surface().get_height() - size) // 2
            rotated_rect = pokeball_rotated.get_rect(center=(x + size // 2, y + size // 2))

            # Limpiar la pantalla y dibujar la Pokéball
            screen.fill((0, 0, 0))
            screen.blit(pokeball_rotated, rotated_rect.topleft)
            pygame.display.flip()

        # Si la animación terminó, cambiar a la pantalla de combate
        if transition_complete:
            from game.screen.combat_screen import CombatScreen
            return CombatScreen(player, enemy_pokemon)

        clock.tick(60)


"""
Funciones para dibujar las cajas de información de los Pokémon en lso combates.
"""


def draw_combat_pokemon_status_box(screen, pokemon, position, is_player_pokemon,
                                   box_width=250, box_height=80, player=None,
                                   pokeball_image=None):
    """
    Dibuja la caja de información de un Pokémon, incluyendo nombre, nivel, HP y barra de experiencia.

    :param screen: Superficie donde se dibuja la caja.
    :param pokemon: Objeto Pokémon que contiene las estadísticas y datos actuales del Pokémon.
    :param position: Tupla con las coordenadas (x, y) de la esquina superior izquierda de la caja.
    :param is_player_pokemon: Indica si es el Pokémon del jugador (True) o del oponente (False).
    :param box_width: Ancho de la caja de información (por defecto 250).
    :param box_height: Altura de la caja de información (por defecto 80).
    :param player: Objeto jugador que contiene el equipo de Pokémon (opcional).
    :param pokeball_image: Imagen de una Pokéball, que se dibuja si el Pokémon pertenece al jugador (opcional).
    """

    # Definición de colores
    colors = {
        "white": (255, 255, 255),
        "light_gray": (240, 240, 240),
        "black": (0, 0, 0),
        "gray": (200, 200, 200),
        "dark_gray": (80, 80, 80),
        "yellow": (255, 255, 0),
        "blue": (0, 0, 255),
        "hp_green": (34, 139, 34),
        "hp_yellow": (255, 255, 0),
        "hp_orange": (255, 165, 0),
        "hp_red": (255, 0, 0),
    }

    # Fuentes de texto
    fonts = {
        "large": pygame.font.Font("../assets/fonts/pokemon.ttf", 32),
        "medium": pygame.font.Font("../assets/fonts/pokemon.ttf", 24),
        "small": pygame.font.Font("../assets/fonts/pokemon.ttf", 15),
    }

    # Ajustar la altura de la caja si es el Pokémon del jugador
    if is_player_pokemon:
        box_height += 25

    # Dibujar el rectángulo de la caja
    pygame.draw.rect(screen, colors["light_gray"], (*position, box_width, box_height))
    pygame.draw.rect(screen, colors["black"], (*position, box_width, box_height), 2)  # Borde negro

    # Dibujar nombre y nivel del Pokémon
    draw_text(screen, fonts["large"], pokemon.name, colors["black"], (position[0] + 10, position[1] + 2))
    draw_text(screen, fonts["medium"], f"Lv. {pokemon.level}", colors["black"],
              (position[0] + box_width - 68, position[1] + 5))

    # Dibujar la barra de HP
    draw_hp_bar(screen, pokemon, position, box_width, colors, fonts["small"])

    # Mostrar la imagen de la Pokéball si el jugador tiene un ejemplar capturado.
    if player and pokeball_image and any(pok == pokemon.name for pok in player.pokedex_captured):
        screen.blit(pokeball_image, (position[0] + 10, position[1] + 44))

    # Dibujar PS actuales y máximos si es el Pokémon del jugador
    if is_player_pokemon:
        draw_hp_text(screen, pokemon, position, box_width, colors["white"], fonts["medium"])

    # Dibujar barra de experiencia si es el Pokémon del jugador
    if is_player_pokemon:
        draw_exp_bar(screen, pokemon, position, box_width, box_height, colors)


def draw_text(screen, font, text, color, position):
    """Dibuja el texto en la pantalla."""
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)


def draw_hp_bar(screen, pokemon, position, box_width, colors, small_font):
    """Dibuja la barra de HP de un Pokémon."""
    hp_bar_position = (position[0] + 110, position[1] + 50)
    hp_bar_width = box_width / 2
    hp_bar_height = 10
    hp_percentage = pokemon.current_hp / pokemon.max_stats['hp']

    # Seleccionar color según porcentaje de HP
    if hp_percentage > 0.5:
        hp_color = colors["hp_green"]
    elif 0.25 < hp_percentage <= 0.5:
        hp_color = colors["hp_yellow"]
    elif 0.125 < hp_percentage <= 0.25:
        hp_color = colors["hp_orange"]
    else:
        hp_color = colors["hp_red"]

    # Dibujar borde de la barra de HP
    hp_bar_border_position = (hp_bar_position[0] - 17, hp_bar_position[1] - 2)
    hp_bar_border_width = hp_bar_width + 19
    hp_bar_border_height = hp_bar_height + 4
    pygame.draw.rect(screen, colors["dark_gray"], (*hp_bar_border_position, hp_bar_border_width, hp_bar_border_height),
                     border_radius=2)

    # Dibujar barra de HP vacía y actual
    pygame.draw.rect(screen, colors["gray"], (*hp_bar_position, hp_bar_width, hp_bar_height), border_radius=1)
    pygame.draw.rect(screen, hp_color, (*hp_bar_position, int(hp_bar_width * hp_percentage), hp_bar_height),
                     border_radius=1)

    # Dibujar el texto "HP"
    draw_text(screen, small_font, "HP", colors["yellow"], (hp_bar_position[0] - 14, hp_bar_position[1] - 4))


def draw_hp_text(screen, pokemon, position, box_width, white, font):
    """Dibuja los PS actuales y máximos si es el Pokémon del jugador."""
    ps_box_width = 135
    ps_box_height = 18
    ps_box_position = (position[0] + 100, position[1] + 68)
    pygame.draw.rect(screen, white, (*ps_box_position, ps_box_width, ps_box_height), border_radius=5)

    hp_text = font.render(f"{pokemon.current_hp}/{pokemon.max_stats['hp']}", True, (0, 0, 0))
    text_rect = hp_text.get_rect(
        center=(ps_box_position[0] + ps_box_width // 2, ps_box_position[1] + ps_box_height // 2))
    screen.blit(hp_text, text_rect)


def draw_exp_bar(screen, pokemon, position, box_width, box_height, colors):
    """Dibuja la barra de experiencia si es el Pokémon del jugador."""
    exp_bar_position = (position[0] + 10, position[1] + box_height - 5)
    exp_bar_width = box_width - 20
    exp_bar_height = 10
    exp_percentage = pokemon.experience / pokemon.experience_to_next_level

    # Dibujar borde y barra de experiencia
    pygame.draw.rect(screen, colors["black"], (*exp_bar_position, exp_bar_width, exp_bar_height), border_radius=2)
    pygame.draw.rect(screen, colors["white"],
                     (exp_bar_position[0] + 2, exp_bar_position[1] + 2, exp_bar_width - 4, exp_bar_height - 4),
                     border_radius=2)
    pygame.draw.rect(screen, colors["blue"], (
        exp_bar_position[0] + 2, exp_bar_position[1] + 2, int((exp_bar_width - 4) * exp_percentage),
        exp_bar_height - 4),
                     border_radius=2)


"""
FUNCIONES PARA CREAR EL MENU DE OPCIONES EN COMBATE
"""


def draw_action_menu(screen, mouse_pos):
    """Dibuja el menú de acciones con 4 opciones estilizadas y devuelve los rects."""
    menu_x = 412
    menu_y = 460
    menu_width = 367
    menu_height = 117

    # Colores de fondo personalizados para cada opción
    option_colors = [
        (178, 34, 34),
        (255, 165, 0),
        (60, 179, 113),
        (70, 130, 180)
    ]

    # Colores para bordes
    white_border_color = (255, 255, 255)
    black_border_color = (0, 0, 0)
    shadow_color = (50, 50, 50)

    # Opciones del menú
    options = ["FIGHT", "BAG", "POKÉMON", "RUN"]

    # Fuente para el texto
    font = pygame.font.Font(utils.load_font(), 42)

    option_rects = []

    # Dibujar las 4 cajas (2x2)
    box_padding = 10
    corner_radius = 15

    for i, option in enumerate(options):
        box_x = menu_x + (i % 2) * (menu_width // 2 + box_padding)
        box_y = menu_y + (i // 2) * (menu_height // 2 + box_padding)

        # Crear el rect de la caja
        box_rect = pygame.Rect(box_x, box_y, menu_width // 2, menu_height // 2)
        option_rects.append(box_rect)

        # Sombra
        pygame.draw.rect(screen, shadow_color, box_rect.move(5, 5).inflate(6, 6), border_radius=corner_radius)

        # Efecto hover
        if box_rect.collidepoint(mouse_pos):
            hover_color = tuple(min(c + 30, 255) for c in option_colors[i])
        else:
            hover_color = option_colors[i]

        # Dibujar el borde externo negro grueso
        pygame.draw.rect(screen, black_border_color, box_rect.inflate(6, 6), border_radius=corner_radius, width=10)

        # Dibujar el borde interno blanco
        pygame.draw.rect(screen, white_border_color, box_rect.inflate(4, 4), border_radius=corner_radius, width=6)

        pygame.draw.rect(screen, hover_color, box_rect, border_radius=corner_radius)

        # Renderizar el texto y colocarlo en el centro de la caja
        text_surface = font.render(option, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=box_rect.center)
        screen.blit(text_surface, text_rect)

    return option_rects


class PokemonCombatMovement:
    def __init__(self, start_pos, end_pos, speed=8, callback_on_complete=None):
        """
        Inicializa el administrador de movimientos.

        :param start_pos: Tupla con la posición inicial (x, y).
        :param end_pos: Tupla con la posición final (x, y).
        :param speed: Velocidad de movimiento en píxeles por frame.
        :param callback_on_complete: Función opcional que se llama cuando se completa el movimiento.
        """
        self.current_pos = list(start_pos)
        self.end_pos = list(end_pos)
        self.speed = speed
        self.movement_complete = False
        self.callback_on_complete = callback_on_complete

    def update(self):
        """Actualiza la posición de la entidad moviéndola hacia su destino."""
        if not self.movement_complete:
            # Calcular la distancia restante
            dx = self.end_pos[0] - self.current_pos[0]
            dy = self.end_pos[1] - self.current_pos[1]

            # Si está cerca del destino, ajustamos la posición directamente
            if abs(dx) < self.speed:
                self.current_pos[0] = self.end_pos[0]
            else:
                # Mueve hacia la dirección x
                self.current_pos[0] += self.speed if dx > 0 else -self.speed

            if abs(dy) < self.speed:
                self.current_pos[1] = self.end_pos[1]
            else:
                # Mueve hacia la dirección y
                self.current_pos[1] += self.speed if dy > 0 else -self.speed

            # Verifica si ha llegado a la posición final
            if self.current_pos == self.end_pos:
                self.movement_complete = True
                if self.callback_on_complete:
                    self.callback_on_complete()

    def has_completed(self):
        """Devuelve True si el movimiento ha sido completado."""
        return self.movement_complete

    def get_position(self):
        """Devuelve la posición actual del objeto que se está moviendo."""
        return self.current_pos


"""
GUARDADO DE PARTIDA
"""


def draw_save_game_box(screen, player, box_position=(30, 30), box_width=400, box_height=300):
    """
    Dibuja una caja de información de guardado de juego con los detalles del jugador, equipo Pokémon y tiempo jugado.

    :param screen: La pantalla en la que se va a dibujar.
    :param player: Objeto del jugador.
    :param box_position: La posición superior izquierda de la caja.
    :param box_width: El ancho de la caja.
    :param box_height: La altura de la caja.
    """
    # Colores
    outer_border_color = (218, 165, 32)
    inner_border_color = (75, 77, 76)
    text_color = (0, 0, 0)
    red_color = (255, 0, 0)
    fill_color = (255, 255, 255)

    # Bordes y radios
    outer_border_thickness = 4
    inner_border_thickness = 4
    outer_border_radius = 8
    inner_border_radius = 5

    # Fuente
    font = pygame.font.Font(utils.load_font(), 35)

    # Crear la superficie para el cuadro de guardado
    save_box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

    # Dibujar el borde dorado exterior
    pygame.draw.rect(save_box_surface, outer_border_color, (0, 0, box_width, box_height),
                     border_radius=outer_border_radius, width=outer_border_thickness)

    # Dibujar el borde grisáceo interior
    pygame.draw.rect(save_box_surface, inner_border_color,
                     (outer_border_thickness, outer_border_thickness,
                      box_width - 2 * outer_border_thickness, box_height - 2 * outer_border_thickness),
                     border_radius=inner_border_radius, width=inner_border_thickness)

    # Dibujar el relleno blanco dentro del cuadro de guardado
    pygame.draw.rect(save_box_surface, fill_color,
                     (outer_border_thickness + inner_border_thickness, outer_border_thickness + inner_border_thickness,
                      box_width - 2 * (outer_border_thickness + inner_border_thickness),
                      box_height - 2 * (outer_border_thickness + inner_border_thickness)),
                     border_radius=5)

    # Blit del cuadro de guardado en la superficie principal
    screen.blit(save_box_surface, box_position)

    # Posiciones de los títulos (izquierda) y valores (derecha)
    left_x = box_position[0] + 30
    right_x = box_position[0] + box_width - 30
    start_y = box_position[1] + 70
    line_spacing = 45

    # Dibujar el título en rojo centrado
    title_text = font.render("POKÉMON GAME", True, red_color)
    screen.blit(title_text, (box_position[0] + (box_width - title_text.get_width()) // 2, box_position[1] + 20))

    # 1. Dibujar la información del jugador en la parte izquierda (PLAYER)
    player_text = font.render("PLAYER:", True, text_color)
    screen.blit(player_text, (left_x, start_y))

    player_name_text = font.render(player.name, True, text_color)
    screen.blit(player_name_text, (right_x - player_name_text.get_width(), start_y))

    # 2. Dibujar la Pokédex (POKÉDEX)
    pokedex_text = font.render("POKÉDEX:", True, text_color)
    screen.blit(pokedex_text, (left_x, start_y + line_spacing))

    pokedex_seen = player.get_pokedex_counts()[0]
    pokedex_count_text = font.render(f"{pokedex_seen}", True, text_color)
    screen.blit(pokedex_count_text, (right_x - pokedex_count_text.get_width(), start_y + line_spacing))

    # 3. Dibujar Pokémon Team (POKÉMON TEAM)
    pokemon_team_text = font.render("POKÉMON TEAM:", True, text_color)
    screen.blit(pokemon_team_text, (left_x, start_y + 2 * line_spacing))

    # Dibujar las imágenes de los Pokémon en el equipo debajo del texto "POKÉMON TEAM"
    pokemon_image_y = start_y + 3 * line_spacing
    pokemon_image_x = left_x
    pokemon_image_size = (40, 40)

    for pokemon in player.pokemons:
        if pokemon.image:
            resized_image = pygame.transform.scale(pokemon.image, pokemon_image_size)
            screen.blit(resized_image, (pokemon_image_x, pokemon_image_y))
            pokemon_image_x += 60

    # 4. Dibujar el tiempo de juego (TIME)
    time_text = font.render("TIME:", True, text_color)
    playtime_text = font.render(player.get_playtime_formatted(), True, text_color)
    screen.blit(time_text, (left_x, pokemon_image_y + 40))
    screen.blit(playtime_text, (right_x - playtime_text.get_width(), pokemon_image_y + 40))


def draw_pokedex_pokemon_slots(screen, player, pokemon_list, current_scroll_position, selected_index, font):
    """Dibuja los slots de los Pokémon en la Pokédex"""

    box_width, box_height = 330, 50  # Tamaño de las cajas
    padding = 10  # Espacio entre las cajas
    border_radius = 25  # Radio de las esquinas redondeadas
    x_position = 460  # Posición en X donde se dibuja el primer slot
    y_position = 80  # Posición en Y donde se empieza a dibujar

    num_pokemon_visible = 8

    for i, pokemon in enumerate(pokemon_list[current_scroll_position:current_scroll_position + num_pokemon_visible]):
        # Determinar la posición Y para cada slot
        y_pos = y_position + i * (box_height + padding)

        # Si el slot es el seleccionado, dibujar la caja
        if current_scroll_position + i == selected_index:
            box_color = (0, 0, 0)
            text_color = (255, 255, 255)

            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surface, box_color, box_surface.get_rect(), border_radius=border_radius)
            screen.blit(box_surface, (x_position, y_pos))  # Dibujar la caja seleccionada
        else:
            # Si no está seleccionada, no dibujamos la caja
            text_color = (0, 0, 0)

        # Cargar y dibujar la imagen del Pokémon
        img_path = f"../assets/pokemon_images/{pokemon['name'].lower()}.png"
        if os.path.exists(img_path):
            image = pygame.image.load(img_path)
            image = pygame.transform.scale(image, (48, 48))
            screen.blit(image, (x_position + 10, y_pos + (box_height - 48) // 2))

        # Dibujar el número de Pokédex
        pokedex_number = font.render(f"Nº. {pokemon['id']}", True, text_color)
        screen.blit(pokedex_number, (x_position + 80, y_pos + (box_height - pokedex_number.get_height()) // 2))

        # Dibujar el nombre del Pokémon
        name_text = font.render(pokemon['name'].capitalize(), True, text_color)
        screen.blit(name_text, (x_position + 160, y_pos + (box_height - name_text.get_height()) // 2))

        # Verificar si el jugador tiene el Pokémon capturado
        if pokemon['name'].capitalize() in player.pokedex_captured:
            # Dibuja la Poké Ball a la derecha del slot
            pokeball_image_path = "../assets/img/icons/pokeball.png"
            pokeball_image = pygame.image.load(pokeball_image_path)
            pokeball_image = pygame.transform.scale(pokeball_image, (28, 28))
            screen.blit(pokeball_image, (x_position + box_width - 40, y_pos + (box_height - 32) // 2))

    # Mostrar en grande el Pokémon seleccionado
    if pokemon_list and 0 <= selected_index < len(pokemon_list):
        selected_pokemon = pokemon_list[selected_index]

        big_image_x = 35
        big_image_y = 90

        # Cargar y dibujar la imagen en tamaño grande
        big_img_path = f"../assets/pokemon_images/{selected_pokemon['name'].lower()}.png"
        if os.path.exists(big_img_path):
            big_image = pygame.image.load(big_img_path)
            big_image = pygame.transform.scale(big_image, (350, 350))
            screen.blit(big_image, (big_image_x, big_image_y))


def draw_scroll_bar(screen, pokemon_list, current_scroll_position, num_pokemon_visible):
    """Dibuja la barra de desplazamiento en la Pokédex."""

    total_pokemon = len(pokemon_list)
    # Rect de la barra de desplazamiento
    scroll_bar_width = 5
    scroll_bar_height = 430
    scroll_bar_x = 792
    scroll_bar_y = 100

    # Calcular la proporción del número de Pokémon visibles respecto al total
    proportion = num_pokemon_visible / total_pokemon if total_pokemon > 0 else 0
    visible_scroll_height = int(scroll_bar_height * proportion)

    # Calcular la posición de la barra de desplazamiento
    scroll_position = (current_scroll_position / (total_pokemon - num_pokemon_visible)) * (
                scroll_bar_height - visible_scroll_height) if total_pokemon > num_pokemon_visible else 0

    # Dibujar la barra de fondo
    pygame.draw.rect(screen, (190, 2, 3), (scroll_bar_x, scroll_bar_y, scroll_bar_width, scroll_bar_height))

    # Dibujar la barra visible
    pygame.draw.rect(screen, (250, 82, 43),
                     (scroll_bar_x, scroll_bar_y + scroll_position, scroll_bar_width, visible_scroll_height))


def draw_pokedex_badges(screen, player, x, y, font, region_range,
                        width=80, height=31, img_path="../assets/img/badges/corona.png", badge_type="captured"):
    """
    Dibuja una caja con el número de Pokémon avistados/capturados de la región actual.
    """
    # Definir el rect del rectángulo
    rect = pygame.Rect(x, y, width, height)

    # Colores
    box_color = (88, 88, 88)
    text_color = (255, 255, 255)

    # Obtener la lista completa de Pokémon con sus IDs
    pokemon_data = utils.load_pokemon_data()

    # Filtrar los Pokémon por región usando sus nombres y mapeando a sus IDs
    if badge_type == "captured":
        pokemon_filtered = [p for p in pokemon_data if p['name'].capitalize()
                            in player.pokedex_captured and region_range[0] <= p['id'] <= region_range[1]]
    else:
        pokemon_filtered = [p for p in pokemon_data if p['name'].capitalize()
                            in player.pokedex_seen and region_range[0] <= p['id'] <= region_range[1]]

    pokemon_count = len(pokemon_filtered)

    # Cambiar el color de la caja si todos los Pokémon están capturados/avistados
    if badge_type == "captured" and pokemon_count == (region_range[1] - region_range[0] + 1):
        box_color = (218, 165, 32)
    elif badge_type == "seen" and pokemon_count == (region_range[1] - region_range[0] + 1):
        box_color = (218, 165, 32)

    # Dibujar la caja con border_radius
    pygame.draw.rect(screen, box_color, rect, border_radius=8)

    # Cargar y dibujar la imagen si existe
    if img_path and os.path.exists(img_path):
        badge_image = pygame.image.load(img_path)
        badge_image = pygame.transform.scale(badge_image, (rect.height - 10, rect.height - 10))
        screen.blit(badge_image, (rect.x + 10, rect.y + 5))

    # Dibujar el número de Pokémon capturados/avistados
    count_text = font.render(f"{pokemon_count}", True, text_color)
    screen.blit(count_text, (rect.x + rect.width - 32, rect.y + rect.height // 2 - count_text.get_height() // 2))
