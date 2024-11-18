import pygame
import game.ui as ui
import game.utils as utils
import time

from game.icons import TypeIcons
from game.pokemon import Pokemon
from game.screen.base_screen import BaseScreen


class PokedexScreen(BaseScreen):

    REGIONS = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Teselia", "National"]

    REGION_ID_RANGES = {
        "Kanto": (1, 151),
        "Johto": (152, 251),
        "Hoenn": (252, 386),
        "Sinnoh": (387, 493),
        "Teselia": (494, 649),
        "National": (1, 649),
    }

    REGION_OFFSETS = {
        "Kanto": 0,
        "Johto": 151,
        "Hoenn": 251,
        "Sinnoh": 386,
        "Teselia": 494,
        "National": 0
    }

    def __init__(self, player, selected_index=0, region_index=0, current_scroll_position=0):
        super().__init__(player)
        self.current_region_index = region_index
        self.font = pygame.font.Font(utils.load_font(), 30)

        # Flechas
        self.arrow_left_rect = None
        self.arrow_right_rect = None

        # Cargar datos de Pokémon
        self.pokemon_data = utils.load_pokemon_data()
        self.filtered_pokemon_data = self.filter_pokemon_by_region()
        self.current_scroll_position = current_scroll_position  # Posición de desplazamiento actual
        self.selected_index = selected_index  # Índice del Pokémon seleccionado dentro de la región
        self.selected_pokemon = None

        # Variables para desplazamiento continuo
        self.is_scrolling = False
        self.scroll_direction = 0
        self.scroll_timer = 0
        self.scroll_delay = 0.12

        self.footer = ui.Footer(buttons=[{"text": "Data", "icon_path": "../assets/img/keyboard/x_blanco.png"}])

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

            # Ver los datos del Pokémon seleccionado si lo presionamos y está disponible
            elif event.key == pygame.K_x:
                if self.selected_pokemon['name'].capitalize() in self.player.pokedex_seen:
                    return PokedexDataScreen(self.player, self.selected_pokemon,self.selected_index,
                                             self.current_region_index, self.current_scroll_position)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                self.is_scrolling = False  # Detener desplazamiento al soltar la tecla

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.arrow_left_rect and self.arrow_left_rect.collidepoint(mouse_pos):
                self.change_region(1)
            elif self.arrow_right_rect and self.arrow_right_rect.collidepoint(mouse_pos):
                self.change_region(-1)

            footer_button = self.footer.handle_events(event)
            if footer_button == "Data":
                if self.selected_pokemon['name'].capitalize() in self.player.pokedex_seen:
                    return PokedexDataScreen(self.player, self.selected_pokemon, self.selected_index,
                                             self.current_region_index, self.current_scroll_position)
            elif footer_button == "Back":
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
        self.selected_pokemon = self.filtered_pokemon_data[self.selected_index]

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

        # Dibujar Pokémon visibles
        ui.draw_pokedex_pokemon_slots(screen, self.player, self.filtered_pokemon_data,
                                      self.REGIONS[self.current_region_index], self.REGION_OFFSETS,
                                      self.current_scroll_position, self.selected_index,
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


class PokedexDataScreen(BaseScreen):
    def __init__(self, player, pokemon, selected_index, region_index, current_scroll_position):
        super().__init__(player)
        self.pokemon = pokemon
        self.selected_index = selected_index
        print(f"Indice: {self.selected_index}")
        self.region_index = region_index
        self.current_scroll_position = current_scroll_position
        self.footer = ui.Footer()

        # Obtenemos los datos de la región actual
        self.region_name = PokedexScreen.REGIONS[self.region_index]
        id_range = PokedexScreen.REGION_ID_RANGES[self.region_name]
        offset = PokedexScreen.REGION_OFFSETS.get(self.region_name, 0)

        # Filtramos Pokémon avistados en esta región y calculamos sus índices regionales
        self.seen_pokemon_data = [
            p for p in utils.load_pokemon_data()
            if id_range[0] <= p['id'] <= id_range[1] and p['name'].capitalize() in self.player.pokedex_seen
        ]
        self.seen_pokemon_ids = [p['id'] - offset - 1 for p in self.seen_pokemon_data]  # region_id basado en offset

        # Calculamos el índice inicial dentro de `seen_pokemon_data` basado en el `selected_index` original
        self.selected_index = next(
            (i for i, p in enumerate(self.seen_pokemon_data) if p['id'] == pokemon['id']),
            0
        )
        # Calculamos el número total de índices en una región
        self.total_indexes_in_region = PokedexScreen.REGION_ID_RANGES[self.region_name][1] - \
                                  PokedexScreen.REGION_ID_RANGES[self.region_name][0]

        # Flechas interactivas
        self.arrow_up_rect = None
        self.arrow_down_rect = None

        # Variables para manejar el sonido del Pokémon
        self.sound_cooldown = 0
        self.pokemon_cry_sound = None
        self.update_pokemon_sound()

    def update_pokemon_sound(self):
        """Actualiza el sonido del Pokémon seleccionado."""
        cry_path = f"../assets/pokemon_sounds/{self.pokemon['name'].lower()}.mp3"
        self.pokemon_cry_sound = pygame.mixer.Sound(cry_path)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.previous_pokemon()

            elif event.key == pygame.K_DOWN:
                self.next_pokemon()

            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                region_id = self.pokemon['id'] - PokedexScreen.REGION_OFFSETS[self.region_name] - 1
                print(f"Region ID: {region_id}")
                self.current_scroll_position = self.total_indexes_in_region - 8 + (self.total_indexes_in_region - region_id)\
                    if region_id >= self.total_indexes_in_region - 3 else region_id - 4 if region_id > 3 else 0


                return PokedexScreen(self.player, selected_index=region_id, region_index=self.region_index,
                                     current_scroll_position=self.current_scroll_position)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Reproducir el sonido del Pokémon al hacer clic en el icono
            cry_icon_rect = pygame.Rect(680, 95, 40, 40)
            if cry_icon_rect.collidepoint(mouse_pos):
                if self.sound_cooldown <= 0:
                    if self.pokemon_cry_sound is not None:
                        self.pokemon_cry_sound.play()
                        self.sound_cooldown = 1

            elif self.arrow_up_rect.collidepoint(mouse_pos):
               self.previous_pokemon()

            elif self.arrow_down_rect.collidepoint(mouse_pos):
                self.next_pokemon()

            elif self.footer.handle_events(event):
                region_id = self.pokemon['id'] - PokedexScreen.REGION_OFFSETS[self.region_name] - 1
                self.current_scroll_position = region_id - 4 if region_id > 4 else 0
                return PokedexScreen(self.player, selected_index=region_id, region_index=self.region_index,
                                     current_scroll_position=self.current_scroll_position)
        return self

    def previous_pokemon(self):
        """Navega al Pokémon avistado anterior en la lista."""
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_pokemon_details()

    def next_pokemon(self):
        """Navega al siguiente Pokémon avistado en la lista."""
        if self.selected_index < len(self.seen_pokemon_data) - 1:
            self.selected_index += 1
            self.update_pokemon_details()

    def update_pokemon_details(self):
        """Actualiza los detalles del Pokémon seleccionado."""
        self.pokemon = self.seen_pokemon_data[self.selected_index]
        self.update_pokemon_sound()

    def update(self):
        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1 / 20

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        stripe_width = 100

        # Fondo
        ui.draw_pokemon_background(screen, [(120 + stripe_width, 0),
                                            (882.73, 0), (580, screen_height),
                                            (-82.73, screen_height)],
                                    [(120, 0),(120 + stripe_width, 0),
                                    (-182.73 + stripe_width, screen_height), (-182.73, screen_height)],
                                   (110, 215), (370, 370), triangle_color=(255, 107, 43),
                                   stripe_color=(255, 70, 32), background_color=(255, 245, 254),
                                   img_path="../assets/img/pokemon_menu/pokedex_fondo.png", angle_rotation=8,
                                   extra_stripe_points=[(screen_width - 120, screen_height),
                                                        (screen_width - 120 - stripe_width, screen_height),
                                                        (882.73, 0), (882.73 + stripe_width,0)])

        # Dibujar el Pokémon seleccionado
        img_path = f"../assets/pokemon_images/{self.pokemon['name'].lower()}.png"
        pokemon_image = pygame.transform.scale(pygame.image.load(img_path), (350, 350))
        screen.blit(pokemon_image, (35, 90))

        # Barra con el nombre del Pokémon, su pokédex ID, género e icono.
        pygame.draw.polygon(screen, (0, 0, 0), [(screen_width/2-50, 30), (screen_width-25, 30), (screen_width-25, 75),
                                                (screen_width/2-50, 75)])
        pygame.draw.polygon(screen, (255, 71, 1),
                            [(screen_width / 2 - 50, 30), (screen_width / 2 + 100, 30), (472, 75),
                             (screen_width / 2 - 50, 75)])

        # Nombre del Pokémon
        name_text = pygame.font.Font(utils.load_font(), 32).render(f"{self.pokemon['name'].capitalize()}", True, (255, 255, 255))
        screen.blit(name_text, (screen_width/2+110, 32))

        # Numero de pokedex
        pokedex_id_text = pygame.font.Font(utils.load_font(), 24).render(f"No. {self.pokemon['id']}", True, (255, 255, 255))
        screen.blit(pokedex_id_text, (screen_width/2+15, 40))

        # Icono del pokemon
        pokemon_image = pygame.transform.scale(pygame.image.load(img_path), (50, 50))
        screen.blit(pokemon_image, (screen_width/2-50, 30))

        # Icono de la pokeball (capturado/avistado)
        if self.pokemon['name'].lower() in (name.lower() for name in self.player.pokedex_captured):
            pokeball_icon_path = "../assets/img/main_menu/icons/pokeball.png"
        else:
            pokeball_icon_path = "../assets/img/pokemon_menu/pokeball_white.png"

        # Cargar y dibujar la imagen de la Poké Ball
        pokeball_icon = pygame.image.load(pokeball_icon_path)
        pokeball_icon = pygame.transform.scale(pokeball_icon, (38, 38))
        screen.blit(pokeball_icon, (screen_width -90, 32))

        # Dibujamos flechas interactivas para pasar de un pokemon a otro
        self.arrow_up_rect = ui.draw_interactive_arrow(screen,
                                                       [(screen_width // 2 + 150, 27), (screen_width // 2 + 162, 17),
                                                        (screen_width // 2 + 174, 27)], (255, 255, 255))
        self.arrow_down_rect = ui.draw_interactive_arrow(screen,
                                                         [(screen_width // 2 + 150, 78), (screen_width // 2 + 162, 88),
                                                          (screen_width // 2 + 174, 78)], (255, 255, 255))

        # Sonido del Pokémon
        ui.draw_box(screen, f"{self.pokemon['name'].capitalize()}'s Cry", screen_width/2-15, 105, screen_width/2 - 50, 50, font_size=25)
        pokemon_cry_icon_path = f"../assets/img/pokemon_menu/pokemon_cry.png"
        pokemon_cry_icon = pygame.transform.scale(pygame.image.load(pokemon_cry_icon_path), (40, 40))
        screen.blit(pokemon_cry_icon, (screen_width-120, 110))

        # Tipos del Pokémon
        icon_manager = TypeIcons(icon_size=(60, 25))
        type_icons = [icon_manager.get_icon(pokemon_type.lower()) for pokemon_type in self.pokemon["types"]]

        pokemon_height = int(self.pokemon['physical_attributes']['height']) / 10
        pokemon_weight = int(self.pokemon['physical_attributes']['weight']) / 10

        pokemon_info = {
            "Type": type_icons,
            "Height": f"{pokemon_height} m",
            "Weight": f"{pokemon_weight} kg",
            "Capture Rate": (
        f"{self.pokemon['species']['capture_rate']}"
        if self.pokemon["name"].lower() in (name.lower() for name in self.player.pokedex_captured)
        else "??"
    ),
        }

        ui.draw_box(screen, pokemon_info, screen_width/2-15, 157, screen_width/2 - 50, 190, font_size=27)

        # Descripción del Pokémon
        pokemon_description = self.pokemon["species"]["description"].replace('\n', ' ').replace('\f', ' ')
        ui.draw_box(screen, pokemon_description, screen_width/2-15, 349, screen_width/2 - 50, 110, font_size=24)

        self.footer.draw(screen)
        pygame.display.flip()
