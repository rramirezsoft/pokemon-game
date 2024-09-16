import pygame
import pygame.gfxdraw
import math

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
                     (border_thickness, border_thickness, box_width - 2 * border_thickness, box_height - 2 * border_thickness),
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


def draw_pokemon_background(screen, triangle_points, stripe_points, pokeball_position, pokemon_size):
    """
    Dibuja un fondo personalizado para el menú de equipo Pokémon.

    :param screen: Superficie de pygame en la que se dibuja el fondo.
    :param triangle_points: Lista de puntos (x, y) para el triángulo rojo.
    :param stripe_points: Lista de puntos (x, y) para la franja diagonal en rojo oscuro.
    :param pokeball_position: Tupla (x, y) para la posición de la Pokéball.
    :param pokemon_size: Tamaño de la pokeball
    """
    # Definir los colores
    red_color = (227, 49, 63)
    dark_red_color = (196, 40, 53)
    soft_blue_gray = (233, 239, 255)

    # Obtener el tamaño de la pantalla
    screen.fill(soft_blue_gray)

    # Dibujar el triángulo rojo brillante
    pygame.draw.polygon(screen, red_color, triangle_points)

    # Dibujar la franja diagonal en rojo oscuro que sea paralela al triángulo
    pygame.draw.polygon(screen, dark_red_color, stripe_points)

    # Dibujar la pokeball de fondo.
    pokeball_image = pygame.image.load('../assets/img/pokemon_menu/info.png')

    # Escalar la imagen de la Pokéball a 600px
    pokeball_scaled = pygame.transform.scale(pokeball_image, pokemon_size)

    # Girar la imagen de la Pokéball un poco (por ejemplo, 15 grados)
    pokeball_rotated = pygame.transform.rotate(pokeball_scaled, 15)

    # Obtener el rectángulo de la imagen rotada para centrarla correctamente
    pokeball_rect = pokeball_rotated.get_rect()
    pokeball_rect.topleft = pokeball_position

    # Dibujar la imagen de la Pokéball
    screen.blit(pokeball_rotated, pokeball_rect.topleft)


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


def draw_combat_pokemon_status_box(screen, pokemon, position, is_player_pokemon=False):
    """
    Dibuja la caja de estado del Pokémon, mostrando su nombre, nivel, barra de vida, PS y barra de experiencia.
    """
    # Tamaño y colores de la caja de estado
    box_width = 300
    box_height = 100
    box_color = (255, 255, 255)  # Fondo blanco
    border_color = (0, 0, 0)  # Borde negro
    text_color = (0, 0, 0)  # Texto negro
    health_bar_color = (50, 205, 50)  # Verde para la barra de vida
    exp_bar_color = (0, 191, 255)  # Azul para la barra de experiencia

    # Fuente
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)

    # Dibuja el fondo de la caja
    pygame.draw.rect(screen, box_color, (*position, box_width, box_height))
    pygame.draw.rect(screen, border_color, (*position, box_width, box_height), 2)

    # Dibuja el nombre y nivel del Pokémon
    name_text = font.render(pokemon.name, True, text_color)
    level_text = font.render(f"Lv. {pokemon.level}", True, text_color)
    screen.blit(name_text, (position[0] + 10, position[1] + 10))
    screen.blit(level_text, (position[0] + box_width - 70, position[1] + 10))

    # Dibuja la barra de vida
    max_health_width = 200  # Ancho máximo de la barra de vida
    current_health_width = int((pokemon.current_hp / pokemon.max_hp) * max_health_width)
    pygame.draw.rect(screen, health_bar_color, (position[0] + 10, position[1] + 50, current_health_width, 10))
    pygame.draw.rect(screen, border_color, (position[0] + 10, position[1] + 50, max_health_width, 10), 2)

    # Si es el Pokémon del jugador, mostrar los PS numéricos y la barra de experiencia
    if is_player_pokemon:
        # Mostrar los PS actuales y máximos
        ps_text = small_font.render(f"{pokemon.current_hp}/{pokemon.max_hp}", True, text_color)
        screen.blit(ps_text, (position[0] + max_health_width + 20, position[1] + 45))

        # Dibuja la barra de experiencia (sin números, solo la barra azul)
        max_exp_width = 180
        current_exp_width = int((pokemon.current_exp / pokemon.next_level_exp) * max_exp_width)
        pygame.draw.rect(screen, exp_bar_color, (position[0] + 10, position[1] + 80, current_exp_width, 5))
        pygame.draw.rect(screen, border_color, (position[0] + 10, position[1] + 80, max_exp_width, 5), 1)