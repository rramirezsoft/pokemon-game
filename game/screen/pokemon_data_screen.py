import pygame
import game.ui as ui
import game.utils as utils


class PokemonDataScreen:
    TAB_INFO = 0
    TAB_STATS = 1
    TAB_MOVES = 2

    def __init__(self, player, pokemon_team, selected_pokemon_index, combat=None):
        """
        Inicializa la pantalla de datos del Pokémon.

        :param player: Objeto Player que contiene la información del jugador y sus Pokémon.
        :param pokemon_team: El equipo de Pokémon del jugador.
        :param selected_pokemon_index: El índice del Pokémon seleccionado en el equipo.
        """
        self.player = player
        self.pokemon_team = pokemon_team  # El equipo de Pokémon
        self.selected_pokemon_index = selected_pokemon_index  # Índice del Pokémon actualmente seleccionado
        self.selected_pokemon = pokemon_team[selected_pokemon_index]  # El Pokémon seleccionado actualmente
        self.combat = combat  # Instancia del combate (si la hay)

        self.current_tab = self.TAB_INFO  # Pestaña abierta por defecto
        self.selected_move_index = None  # Índice del movimiento seleccionado
        self.move_rects = []  # Rectángulos de los movimientos para detección de clics

        # Imagen de la Pokébola para el fondo
        self.pokeball_image = utils.load_image("../assets/img/icons/pokeball.png", (26, 26))

        # Fuente para el texto
        self.font = pygame.font.Font(utils.load_font(), 30)

        # Flechas
        self.arrow_up_rect = None
        self.arrow_down_rect = None
        self.arrow_left_rect = None
        self.arrow_right_rect = None

        # Crear el footer
        self.footer = ui.Footer(text="Back")
        self.footer.footer_rect.topleft = (0, 575)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:

            # Para cambiar de pestaña dentro de un pokemon
            if event.key == pygame.K_LEFT:
                self.current_tab = (self.current_tab - 1) % 3  # Cambia a la pestaña anterior
            elif event.key == pygame.K_RIGHT:
                self.current_tab = (self.current_tab + 1) % 3  # Cambia a la siguiente pestaña

            # Si estamos en la pestaña de movimientos y hay un movimiento seleccionado
            if self.current_tab == self.TAB_MOVES and self.selected_move_index is not None:
                if event.key == pygame.K_DOWN:
                    # Mover al siguiente movimiento
                    self.selected_move_index = (self.selected_move_index + 1) % len(self.selected_pokemon.moves)
                elif event.key == pygame.K_UP:
                    # Mover al movimiento anterior
                    self.selected_move_index = (self.selected_move_index - 1) % len(self.selected_pokemon.moves)

            # Si no estamos en la pestaña de movimientos y presionas flecha abajo, mostrar el siguiente Pokémon
            elif event.key == pygame.K_DOWN:
                self.selected_pokemon_index = (self.selected_pokemon_index + 1) % len(self.pokemon_team)
                self.selected_pokemon = self.pokemon_team[self.selected_pokemon_index]
                self.selected_move_index = None

            # Si presionas flecha arriba, mostrar el Pokémon anterior
            elif event.key == pygame.K_UP:
                self.selected_pokemon_index = (self.selected_pokemon_index - 1) % len(self.pokemon_team)
                self.selected_pokemon = self.pokemon_team[self.selected_pokemon_index]
                self.selected_move_index = None

            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                if self.selected_move_index is not None:
                    self.selected_move_index = None  # Des-seleccionar movimiento
                else:
                    from game.screen.pokemon_menu_screen import PokemonMenuScreen
                    if self.combat:
                        return PokemonMenuScreen(self.player, self.combat)
                    return PokemonMenuScreen(self.player)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Si se hace clic en la flecha izquierda
            if self.arrow_left_rect.collidepoint(mouse_pos):
                self.current_tab = (self.current_tab - 1) % 3

            # Si se hace clic en la flecha derecha
            if self.arrow_right_rect.collidepoint(mouse_pos):
                self.current_tab = (self.current_tab + 1) % 3

            # Llama a las funciones de acción si se hace clic en el área de las flechas (arriba y abajo)
            if self.arrow_up_rect.collidepoint(mouse_pos):
                self.selected_move_index = None
                self.previous_pokemon()
            elif self.arrow_down_rect.collidepoint(mouse_pos):
                self.selected_move_index = None
                self.next_pokemon()

            if self.current_tab == self.TAB_MOVES:
                # Verificar clic en los rectángulos de los movimientos
                for index, rect in enumerate(self.move_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_move_index = index
                        break

            # Manejo del evento del footer
        if self.footer.handle_events(event):
            if self.selected_move_index is not None:
                self.selected_move_index = None  # Des-seleccionar el movimiento
            else:
                from game.screen.pokemon_menu_screen import PokemonMenuScreen
                if self.combat:
                    return PokemonMenuScreen(self.player, self.combat)
                return PokemonMenuScreen(self.player)

        return self

    def previous_pokemon(self):
        """
        Cambia al Pokémon anterior en la lista.
        """
        self.selected_pokemon_index = (self.selected_pokemon_index - 1) % len(self.pokemon_team)
        self.selected_pokemon = self.pokemon_team[self.selected_pokemon_index]

    def next_pokemon(self):
        """
        Cambia al siguiente Pokémon en la lista.
        """
        self.selected_pokemon_index = (self.selected_pokemon_index + 1) % len(self.pokemon_team)
        self.selected_pokemon = self.pokemon_team[self.selected_pokemon_index]

    def update(self):
        pass

    def draw(self, screen):
        """
        Dibuja la pantalla de datos del Pokémon seleccionado.
        """
        screen_width, screen_height = screen.get_size()
        stripe_width = 90  # El ancho de la franja
        ui.draw_pokemon_background(screen, [(0, 0), (screen_width // 2 - 50, 0), (0, screen_height + 300)],
                                   [(screen_width // 2 - 50, 0),
                                    (screen_width // 2 - 50 + stripe_width, 0),
                                    (stripe_width, screen_height + 300), (0, screen_height + 300)],
                                   (380, 220), (400, 400))

        # Dibujar la barra con el nombre y el nivel del pokemon
        pygame.draw.polygon(screen, (0, 0, 0), [(screen_width // 2 + 60, 18), (screen_width, 18),
                                                (screen_width, 53), (screen_width // 2 + 46.39, 53)])
        # Dibujar la pokeball dentro de la barra.
        screen.blit(self.pokeball_image, (screen_width // 2 + 62, 22))

        # Dibujar el nombre y nivel del Pokémon
        name_text = self.font.render(f"{self.selected_pokemon.name}", True, (255, 255, 255))
        font_level = pygame.font.Font(utils.load_font(), 28)
        level_text = self.font.render(f"Nv. {self.selected_pokemon.level}", True, (255, 255, 255))
        screen.blit(name_text, (screen_width // 2 + 120, 15))
        screen.blit(level_text, (screen_width // 2 + 250, 15))

        # Dibujar el Pokémon seleccionado en el centro-derecha de la pantalla
        if self.selected_pokemon.image:
            screen_width, screen_height = screen.get_size()
            max_image_size = (360, 360)
            pokemon_image = pygame.transform.scale(self.selected_pokemon.image, max_image_size)
            x_position = (screen_width - pokemon_image.get_width()) // 2 + 200
            y_position = (screen_height - pokemon_image.get_height()) // 2 + 50
            screen.blit(pokemon_image, (x_position, y_position))

        # Dibujar flechas interactivas
        self.arrow_up_rect = ui.draw_interactive_arrow(screen,
                                                       [(screen_width // 2 + 63, 14), (screen_width // 2 + 75, 4),
                                                        (screen_width // 2 + 87, 14)], (227, 49, 63),
                                                       action=self.previous_pokemon)
        self.arrow_down_rect = ui.draw_interactive_arrow(screen,
                                                         [(screen_width // 2 + 63, 57), (screen_width // 2 + 75, 67),
                                                          (screen_width // 2 + 87, 57)], (227, 49, 63),
                                                         action=self.next_pokemon)
        self.arrow_left_rect = ui.draw_interactive_arrow(screen, [(42, 28), (54, 16), (54, 40)], (255, 255, 255))
        self.arrow_right_rect = ui.draw_interactive_arrow(screen, [(218, 16), (218, 40), (230, 28)], (255, 255, 255))

        # Dibujar los iconos de las opciones de datos a mostrar.
        ui.draw_interactive_icon(screen, "../assets/img/pokemon_menu/info.png", (34, 34), (70, 10))
        ui.draw_interactive_icon(screen, "../assets/img/pokemon_menu/stats.png", (34, 34), (120, 10))
        ui.draw_interactive_icon(screen, "../assets/img/pokemon_menu/moves.png", (39, 39), (168, 9))

        # Dibujar los menus
        if self.current_tab == self.TAB_INFO:
            ui.draw_info_tab(screen, pygame.Rect(0, 53, 430, 280), 24, self.selected_pokemon, self.player)
        elif self.current_tab == self.TAB_STATS:
            ui.draw_stats_tb(screen, pygame.Rect(0, 53, 430, 280), 22, self.selected_pokemon)
        elif self.current_tab == self.TAB_MOVES:
            self.move_rects = ui.draw_moves_tab(screen, self.selected_pokemon, (30, 53),
                                                25, self.selected_move_index)

            if self.selected_move_index is not None:
                move = self.selected_pokemon.moves[self.selected_move_index]

                text_values = {
                    "Class": move.get('damage_class', 'N/A'),
                    "Power": move.get('power', 'N/A'),
                    "Accuracy": move.get('accuracy', 'N/A'),
                }
                ui.draw_rectangles(screen, 0, 320, 430, 40, 3, 0, (255, 255, 255), 24, text_values)

                # Dibujar la descripción del movimiento justo debajo
                description = move.get('description', 'No description available.')
                ui.draw_description(screen, description, 0, 449, 430, 100,
                                    24)

        # Dibujar el footer
        self.footer.draw(screen)

        pygame.display.flip()
