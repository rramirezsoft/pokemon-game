import pygame
import pygame.gfxdraw
import utils as utils


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
                pokemon.current_stats['hp'],
                pokemon.current_stats['hp'],
                health_bar_rect,
                selected=self.selected  # Pasar el estado de selección a HealthBar
            )

    def draw(self, screen):
        """
        Dibuja el slot del Pokémon en la pantalla.

        :param screen: Superficie de pygame en la que se dibuja.
        """
        # Cambiar color de fondo y texto dependiendo de la selección
        bg_color = (0, 0, 0) if self.selected else (255, 255, 255)
        text_color = (255, 255, 255) if self.selected else (0, 0, 0)

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
        self.options = options if options else ["Estadísticas", "Mover", "Atrás"]
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

