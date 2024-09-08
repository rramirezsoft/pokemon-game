import pygame
from game.ui import Footer
import game.utils as utils


def draw_data_background(screen):
    """
    Dibuja el fondo personalizado para la pantalla de estadísticas del Pokémon.

    - La izquierda tendrá secciones claras para las estadísticas.
    - La derecha tendrá espacio estructurado para mostrar la imagen del Pokémon.

    :param screen: Superficie de pygame en la que se dibuja el fondo.
    """
    # Definir los colores
    soft_blue_gray = (230, 230, 255)  # Gris/Azul claro muy suave, casi blanco
    red_color = (255, 86, 86)  # Rojo brillante
    dark_blue = (0, 12, 31)  # Azul oscuro
    light_gray = (210, 210, 230)  # Gris claro
    separator_color = (180, 180, 200)  # Color para separadores

    # Obtener el tamaño de la pantalla
    screen_width, screen_height = screen.get_size()

    # Fondo general de toda la pantalla
    screen.fill(dark_blue)

    # Crear la sección izquierda para las estadísticas (ocupa el 30% de la pantalla)
    stats_section_width = screen_width * 0.3
    pygame.draw.rect(screen, soft_blue_gray, (0, 0, stats_section_width, screen_height))

    # Divisiones en la sección de estadísticas
    section_height = screen_height // 6  # Seis secciones iguales para stats y movimientos
    for i in range(6):
        y = i * section_height
        pygame.draw.rect(screen, light_gray, (10, y + 10, stats_section_width - 20, section_height - 20))
        pygame.draw.line(screen, separator_color, (10, y + section_height), (stats_section_width - 10, y + section_height), 2)

    # Crear una franja diagonal en rojo brillante (similar al estilo anterior)
    diagonal_stripe_points = [
        (stats_section_width - 50, 0),
        (stats_section_width + 50, 0),
        (screen_width, screen_height),
        (screen_width - 100, screen_height)
    ]
    pygame.draw.polygon(screen, red_color, diagonal_stripe_points)

    # Sección derecha (zona para mostrar el Pokémon grande)
    right_section_x = stats_section_width + 50
    right_section_width = screen_width - right_section_x
    pygame.draw.rect(screen, dark_blue, (right_section_x, 0, right_section_width, screen_height), 5)  # Marco


class PokemonDataScreen:
    def __init__(self, player, selected_pokemon):
        """
        Inicializa la pantalla de datos del Pokémon.

        :param player: Objeto Player que contiene la información del jugador y sus Pokémon.
        :param selected_pokemon: El Pokémon que se ha seleccionado para mostrar sus datos.
        """
        self.player = player
        self.selected_pokemon = selected_pokemon

        # Imagen de la Pokébola para el fondo
        self.pokeball_image = pygame.image.load("../assets/img/icons/pokeball.png")
        self.pokeball_image = pygame.transform.scale(self.pokeball_image, (60, 60))

        # Fuente para el texto
        self.font = pygame.font.Font(utils.load_font(), 30)

        # Crear el footer
        self.footer = Footer(text="Atrás")
        self.footer.footer_rect.topleft = (0, 575)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                from game.screen.pokemon_menu_screen import PokemonMenuScreen
                return PokemonMenuScreen(self.player)

        # Manejo del evento del footer
        if self.footer.handle_events(event):
            # Volver a la pantalla del menú Pokémon
            from game.screen.pokemon_menu_screen import PokemonMenuScreen
            return PokemonMenuScreen(self.player)

        return self

    def update(self):
        pass

    def draw(self, screen):
        """
        Dibuja la pantalla de datos del Pokémon seleccionado.
        """
        draw_data_background(screen)

        # Dibujar la imagen de la Pokébola en la esquina superior izquierda
        pokeball_x = 20
        pokeball_y = 20
        screen.blit(self.pokeball_image, (pokeball_x, pokeball_y))

        # Dibujar el nombre y nivel del Pokémon
        name_text = self.font.render(f"{self.selected_pokemon.name}", True, (0, 0, 0))
        level_text = self.font.render(f"Nivel: {self.selected_pokemon.level}", True, (0, 0, 0))
        screen.blit(name_text, (30, 100))
        screen.blit(level_text, (30, 150))

        # Dibujar el Pokémon seleccionado en el centro-derecha de la pantalla
        if self.selected_pokemon.image:
            screen_width, screen_height = screen.get_size()
            max_image_size = (370, 370)
            pokemon_image = pygame.transform.scale(self.selected_pokemon.image, max_image_size)
            x_position = (screen_width - pokemon_image.get_width()) // 2 + 180
            y_position = (screen_height - pokemon_image.get_height()) // 2
            screen.blit(pokemon_image, (x_position, y_position))

        # Dibujar el footer
        self.footer.draw(screen)

        pygame.display.flip()
