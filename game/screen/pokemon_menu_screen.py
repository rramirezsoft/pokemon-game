import pygame
from game.ui import PokemonSlot, Footer
import game.utils as utils


def draw_custom_background(screen):
    """
    Dibuja un fondo personalizado

    - La izquierda será roja con una franja diagonal en rojo oscuro.
    - El triángulo superior izquierdo será rojo y el inferior derecho un tono suave gris/azul.

    :param screen: Superficie de pygame en la que se dibuja el fondo.
    """
    # Definir los colores
    red_color = (255, 0, 0)  # Rojo brillante
    dark_red_color = (139, 0, 0)  # Rojo oscuro (franja diagonal)
    soft_blue_gray = (230, 230, 255)  # Gris/Azul claro muy suave, casi blanco

    # Obtener el tamaño de la pantalla
    screen_width, screen_height = screen.get_size()

    # Crear un polígono en la mitad izquierda con rojo brillante
    left_triangle_points = [(0, 0), (screen_width // 2, 0), (0, screen_height)]
    pygame.draw.polygon(screen, red_color, left_triangle_points)

    # Crear el triángulo inferior derecho en gris/azul claro
    right_triangle_points = [(screen_width // 2, 0), (screen_width, screen_height), (0, screen_height)]
    pygame.draw.polygon(screen, soft_blue_gray, right_triangle_points)

    # Dibujar la franja diagonal en rojo oscuro
    stripe_points = [(screen_width // 2 - 20, 0), (screen_width // 2 + 20, 0),
                     (screen_width, screen_height), (screen_width - 40, screen_height)]
    pygame.draw.polygon(screen, dark_red_color, stripe_points)


class PokemonMenuScreen:
    def __init__(self, player):
        """
        Inicializa la pantalla del menú de Pokémon con los 6 slots dispuestos en 1 columna.

        :param player: Objeto Player que contiene la información del jugador y sus Pokémon.
        """
        self.player = player  # Objeto Player que contiene el equipo del jugador
        self.pokemon_team = self.player.pokemons  # Lista de los Pokémon del jugador (máx 6)
        self.slots = []  # Lista para almacenar los slots de los Pokémon
        self.selected_index = 0  # Índice del slot seleccionado

        # Definir el tamaño y posición de cada slot
        slot_width = 300  # Ancho de cada slot
        slot_height = 70  # Altura de cada slot
        y_padding = 10  # Espacio vertical entre filas
        start_x = 50  # Posición inicial en X (cerca del borde izquierdo)
        start_y = 95  # Posición inicial en Y

        # Crear las posiciones de los 6 slots en una sola columna
        for index in range(6):
            x_pos = start_x
            y_pos = start_y + index * (slot_height + y_padding)
            pokemon = self.pokemon_team[index] if index < len(self.pokemon_team) else None
            slot_rect = pygame.Rect(x_pos, y_pos, slot_width, slot_height)
            slot = PokemonSlot(pokemon, slot_rect, selected=(index == self.selected_index))
            self.slots.append(slot)

        # Cargar y ajustar la imagen de la Pokébola
        self.pokeball_image = pygame.image.load("../assets/img/icons/pokeball.png")
        self.pokeball_image = pygame.transform.scale(self.pokeball_image,
                                                     (60, 60))  # Ajusta el tamaño según lo necesario

        # Cargar la fuente para el texto
        self.font = pygame.font.Font(utils.load_font(), 65)
        self.pokemon_text_surface = self.font.render("EQUIPO POKÉMON", True, (0, 0, 0))

        # Crear el footer
        self.footer = Footer(text="Atrás")

        # Posicionar el footer en la parte inferior de la pantalla
        self.footer.footer_rect.topleft = (0, 575)  # Ajustar según el alto de la pantalla

    def handle_events(self, event):
        """
        Maneja eventos, como clics del ratón o teclas.

        :param event: Evento de pygame.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
        elif self.footer.handle_events(event):
            from game.screen.main_menu_screen import MainMenuScreen  # Importación local
            return MainMenuScreen(self.player)  # Volver al menú principal

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                # Mover la selección hacia abajo
                self.selected_index = (self.selected_index + 1) % len(self.slots)
                self.update()
            elif event.key == pygame.K_UP:
                # Mover la selección hacia arriba
                self.selected_index = (self.selected_index - 1) % len(self.slots)
                self.update()

        return self

    def update(self):
        """
        Actualiza el estado de selección de los slots.
        """
        for index, slot in enumerate(self.slots):
            slot.selected = (index == self.selected_index)

    def draw(self, screen):
        """
        Dibuja la pantalla del menú de Pokémon con los 6 slots.

        :param screen: Superficie de pygame en la que se dibuja.
        """
        # Dibujar el fondo personalizado
        draw_custom_background(screen)

        # Dibujar la imagen de la Pokébola
        pokeball_x = 20
        pokeball_y = 20  # Posición vertical de la Pokébola
        screen.blit(self.pokeball_image, (pokeball_x, pokeball_y))

        # Dibujar el texto "POKÉMON"
        text_x = 100
        text_y = 10
        screen.blit(self.pokemon_text_surface, (text_x, text_y))

        # Dibujar cada slot
        for slot in self.slots:
            slot.draw(screen)

        # Dibujar la imagen del Pokémon preseleccionado a la derecha de la pantalla
        if self.pokemon_team and self.selected_index < len(self.pokemon_team):
            selected_pokemon = self.pokemon_team[self.selected_index]
            if selected_pokemon.image:
                # Ajustar la imagen del Pokémon a un tamaño más grande pero dinámico
                screen_width, screen_height = screen.get_size()
                max_image_size = (370, 370)  # Tamaño máximo para las imágenes de los Pokémon

                # Escalar la imagen si es necesario
                pokemon_image = pygame.transform.scale(selected_pokemon.image, max_image_size)

                # Calcular la posición para centrar la imagen horizontalmente
                x_position = (screen_width - pokemon_image.get_width()) // 2 + 180  # Ajuste a la derecha
                y_position = (screen_height - pokemon_image.get_height()) // 2  # Centrado verticalmente

                # Dibujar la imagen del Pokémon
                screen.blit(pokemon_image, (x_position, y_position))

        # Dibujar el footer
        self.footer.draw(screen)

        # Actualizar la pantalla
        pygame.display.flip()
