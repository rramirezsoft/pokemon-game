import pygame
import game.ui as ui
import game.utils as utils
import time


class PokedexScreen:
    REGIONS = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Teselia", "Nacional"]
    REGION_ID_RANGES = {
        "Kanto": (1, 151),
        "Johto": (152, 251),
        "Hoenn": (252, 386),
        "Sinnoh": (387, 493),
        "Teselia": (494, 649),
        "Nacional": (1, 649),
    }

    def __init__(self, player):
        self.player = player
        self.current_region_index = 0
        self.font = pygame.font.Font(utils.load_font(), 30)

        # Flechas
        self.arrow_left_rect = None
        self.arrow_right_rect = None

        # Cargar datos de Pokémon
        self.pokemon_data = utils.load_pokemon_data()
        self.filtered_pokemon_data = self.filter_pokemon_by_region()
        self.current_scroll_position = 0  # Posición de desplazamiento actual
        self.selected_index = 0  # Índice del Pokémon seleccionado dentro de la región

        # Variables para desplazamiento continuo
        self.is_scrolling = False
        self.scroll_direction = 0
        self.scroll_timer = 0
        self.scroll_delay = 0.15

        self.footer = ui.Footer(text="Back")
        self.footer.footer_rect.topleft = (0, 575)

    def filter_pokemon_by_region(self):
        """Filtrar Pokémon según la región actual basada en sus IDs."""
        region_name = self.REGIONS[self.current_region_index]
        id_range = self.REGION_ID_RANGES[region_name]

        return [p for p in self.pokemon_data if id_range[0] <= p['id'] <= id_range[1]]

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)

            # Cambiar de región con las teclas de flecha izquierda y derecha
            elif event.key == pygame.K_LEFT:
                self.change_region(-1)
            elif event.key == pygame.K_RIGHT:
                self.change_region(1)

            # Navegar entre Pokémon visibles
            elif event.key == pygame.K_DOWN:
                self.is_scrolling = True
                self.scroll_direction = 1
            elif event.key == pygame.K_UP:
                self.is_scrolling = True
                self.scroll_direction = -1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                self.is_scrolling = False  # Detener desplazamiento al soltar la tecla

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.arrow_left_rect and self.arrow_left_rect.collidepoint(mouse_pos):
                self.change_region(-1)
            elif self.arrow_right_rect and self.arrow_right_rect.collidepoint(mouse_pos):
                self.change_region(1)

            if self.footer.handle_events(event):
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)

        return self

    def change_region(self, direction):
        """ Cambia de región según la dirección (-1 para izquierda, 1 para derecha). """
        self.current_region_index = (self.current_region_index + direction) % len(self.REGIONS)
        self.filtered_pokemon_data = self.filter_pokemon_by_region()  # Actualizar lista filtrada al cambiar de región
        self.current_scroll_position = 0  # Reiniciar la posición de desplazamiento al cambiar de región
        self.selected_index = 0  # Reiniciar el índice seleccionado

    def update(self):
        """Actualiza la pantalla para el desplazamiento continuo."""
        current_time = time.time()

        # Controlar el delay entre scrolls
        if self.is_scrolling and current_time - self.scroll_timer > self.scroll_delay:
            self.scroll_timer = current_time

            if self.scroll_direction == 1:  # Desplazar hacia abajo
                if self.selected_index < len(self.filtered_pokemon_data) - 1:
                    self.selected_index += 1

                    # Si el seleccionado está fuera de la vista, hacer scroll
                    if self.selected_index >= self.current_scroll_position + 8:
                        self.current_scroll_position += 1

            elif self.scroll_direction == -1:  # Desplazar hacia arriba
                if self.selected_index > 0:
                    self.selected_index -= 1

                    # Si el seleccionado está fuera de la vista, hacer scroll
                    if self.selected_index < self.current_scroll_position:
                        self.current_scroll_position -= 1

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        stripe_width = 100

        # Fondo
        ui.draw_pokemon_background(screen, [(screen_width // 2 + 100 + stripe_width, 0),
                                            (screen_width, 0), (screen_width, screen_height + 450),
                                            (stripe_width - 30, screen_height + 450)],
                                   [(screen_width // 2 + 100, 0),
                                    (screen_width // 2 + 100 + stripe_width, 0),
                                    (stripe_width - 30, screen_height + 450), (-30, screen_height + 450)],
                                   (425, 215), (370, 370), triangle_color=(255, 107, 43),
                                   stripe_color=(255, 70, 32), background_color=(255, 245, 254),
                                   img_path="../assets/img/pokemon_menu/pokedex_fondo.png", angle_rotation=8)

        # Dibujar la barra con el nombre de la región
        pygame.draw.polygon(screen, (50, 50, 50), [(screen_width // 2 + 90, 18), (screen_width, 18),
                                                   (screen_width, 53), (screen_width // 2 + 73, 53)])
        pygame.draw.polygon(screen, (221, 213, 228), [(0, 18), (screen_width // 2 + 90, 18),
                                                      (screen_width // 2 + 73, 53), (0, 53)])

        # Dibujar texto pokedex
        text = self.font.render("POKÉDEX", True, (0, 0, 0))
        screen.blit(text, (30, 18))

        # Dibujar el nombre de la región seleccionada
        region_name = self.REGIONS[self.current_region_index]
        region_text = self.font.render(region_name, True, (255, 255, 255))
        screen.blit(region_text, (screen_width // 2 + 210, 18))

        # Dibujar flechas a ambos lados del nombre
        self.arrow_left_rect = ui.draw_interactive_arrow(screen,
                                                         [(screen_width // 2 + 310, 26),
                                                          (screen_width // 2 + 325, 35.5),
                                                          (screen_width // 2 + 310, 45)],
                                                         (255, 255, 255))
        self.arrow_right_rect = ui.draw_interactive_arrow(screen,
                                                          [(screen_width // 2 + 180, 26),
                                                           (screen_width // 2 + 165, 35.5),
                                                           (screen_width // 2 + 180, 45)],
                                                          (255, 255, 255))

        # Dibujar Pokémon visibles usando el nuevo método en ui
        ui.draw_pokedex_pokemon_slots(screen, self.player, self.filtered_pokemon_data,
                                      self.current_scroll_position,
                                      self.selected_index,
                                      pygame.font.Font(utils.load_font(), 24))

        # Dibujar la barra de desplazamiento
        ui.draw_scroll_bar(screen, self.filtered_pokemon_data,
                           self.current_scroll_position, 8)

        region_range = self.REGION_ID_RANGES[region_name]  # Obtenemos el rango de IDs entre regiones

        # Dibujar la insignia de Pokémon avistados
        ui.draw_pokedex_badges(screen, self.player, 180, 20, pygame.font.Font(utils.load_font(), 20),
                               region_range, img_path="../assets/img/badges/lupa.png", badge_type="seen")

        # Dibujar la insignia de Pokémon capturados
        ui.draw_pokedex_badges(screen, self.player, 270, 20, pygame.font.Font(utils.load_font(), 20),
                               region_range, badge_type="captured")

        # Dibujar el footer
        self.footer.draw(screen)

        pygame.display.flip()
