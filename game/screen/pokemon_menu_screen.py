import pygame
from game.ui import PokemonSlot, Footer, MiniMenu
import game.utils as utils


def draw_custom_background(screen):
    """
    Dibuja un fondo personalizado

    - La izquierda será roja con una franja diagonal en rojo oscuro.
    - El triángulo superior izquierdo será rojo y el inferior derecho un tono suave gris/azul.

    :param screen: Superficie de pygame en la que se dibuja el fondo.
    """
    # Definir los colores
    red_color = (255, 86, 86)  # Rojo brillante
    dark_red_color = (139, 0, 0)  # Rojo oscuro (franja diagonal)
    soft_blue_gray = (230, 230, 255)  # Gris/Azul claro muy suave, casi blanco

    # Obtener el tamaño de la pantalla
    screen_width, screen_height = screen.get_size()

    screen.fill((0, 12, 31))

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
        self.player = player
        self.pokemon_team = self.player.pokemons
        self.slots = []
        self.selected_index = 0  # Índice del slot preseleccionado
        self.slot_selected = None  # Almacena la caja que está seleccionada
        self.show_menu = False  # Controla si se muestra el mini menú

        slot_width = 300
        slot_height = 70
        y_padding = 10
        start_x = 50
        start_y = 95

        for index in range(6):
            x_pos = start_x
            y_pos = start_y + index * (slot_height + y_padding)
            pokemon = self.pokemon_team[index] if index < len(self.pokemon_team) else None
            slot_rect = pygame.Rect(x_pos, y_pos, slot_width, slot_height)
            slot = PokemonSlot(pokemon, slot_rect, selected=(index == self.selected_index))
            self.slots.append(slot)

        # Imagen de la Pokébola
        self.pokeball_image = pygame.image.load("../assets/img/icons/pokeball.png")
        self.pokeball_image = pygame.transform.scale(self.pokeball_image, (60, 60))

        # Fuente para el texto
        self.font = pygame.font.Font(utils.load_font(), 65)
        self.pokemon_text_surface = self.font.render("EQUIPO POKÉMON", True, (0, 0, 0))

        # Crear el footer
        self.footer = Footer(text="Atrás")
        self.footer.footer_rect.topleft = (0, 575)

        # Crear minimenu
        self.mini_menu = MiniMenu(position=(0, 0), size=(120, 100), options=["Datos", "Mover", "Atrás"])

    def handle_events(self, event):
        """
        Maneja eventos como clics del ratón o teclas.
        """
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if self.slot_selected is None:  # Solo permite mover la preselección si no hay selección activa
                if event.key == pygame.K_DOWN:
                    # Mover preselección hacia abajo
                    self.selected_index = (self.selected_index + 1) % len(self.slots)
                    self.update_preselection()

                elif event.key == pygame.K_UP:
                    # Mover preselección hacia arriba
                    self.selected_index = (self.selected_index - 1) % len(self.slots)
                    self.update_preselection()

                elif event.key == pygame.K_RETURN:
                    # Seleccionar la caja preseleccionada
                    self.select_current_slot()

                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    if self.slot_selected is not None:
                        # Deseleccionar la caja y ocultar el menú
                        self.deselect_slot()
                    else:
                        # Salir de la pantalla si no hay selección activa
                        from game.screen.main_menu_screen import MainMenuScreen
                        return MainMenuScreen(self.player)

            elif self.show_menu:
                # Manejo de eventos para el mini menú
                if event.key == pygame.K_DOWN:
                    # Mover la selección hacia abajo en el mini menú
                    self.mini_menu.selected_index = (self.mini_menu.selected_index + 1) % len(self.mini_menu.options)

                elif event.key == pygame.K_UP:
                    # Mover la selección hacia arriba en el mini menú
                    self.mini_menu.selected_index = (self.mini_menu.selected_index - 1) % len(self.mini_menu.options)

                elif event.key == pygame.K_RETURN:
                    # Ejecutar la opción seleccionada en el mini menú
                    self.execute_mini_menu_option()

                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    # Deseleccionar la caja y ocultar el mini menú
                    self.deselect_slot()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Detectar clic en una caja
            mouse_pos = event.pos
            for index, slot in enumerate(self.slots):
                if slot.rect.collidepoint(mouse_pos):
                    if self.slot_selected is None:  # Si no hay selección activa
                        if index == self.selected_index:
                            # Si se hace clic en la caja preseleccionada, seleccionarla
                            self.select_current_slot()
                        else:
                            # Si se hace clic en otra caja, preseleccionarla
                            self.selected_index = index
                            self.update_preselection()
                    elif index == self.slot_selected:
                        # Si la caja seleccionada se clickea de nuevo, cerrar el menú
                        self.deselect_slot()

            # Manejo del clic en el mini menú
            if self.show_menu:
                option_index = self.mini_menu.is_option_clicked(mouse_pos)
                if option_index is not None:
                    # Cambiar la opción seleccionada
                    self.mini_menu.selected_index = option_index
                    # Ejecutar la opción seleccionada en el mini menú
                    self.execute_mini_menu_option()

        # Manejo del evento del footer
        if self.footer.handle_events(event):
            if self.slot_selected is not None:
                # Deseleccionar la caja si está seleccionada
                self.deselect_slot()
            else:
                # Salir de la pantalla si no hay selección activa
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)

        return self

    def execute_mini_menu_option(self):
        """ Ejecuta la opción seleccionada en el mini menú. """
        option = self.mini_menu.options[self.mini_menu.selected_index]

        if option == "Atrás":
            if self.slot_selected is None:
                # Regresar a la pantalla anterior
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)
            else:
                # Deseleccionar la caja y ocultar el menú
                self.deselect_slot()
        elif option == "Estadísticas":
            # Implementa la funcionalidad para "Estadísticas" aquí
            print("Seleccionada opción: Estadísticas")
        elif option == "Mover":
            # Implementa la funcionalidad para "Mover" aquí
            print("Seleccionada opción: Mover")

    def update_preselection(self):
        """
        Actualiza la preselección de las cajas.
        """
        for index, slot in enumerate(self.slots):
            slot.selected = (index == self.selected_index)

    def update(self):
        pass

    def select_current_slot(self):
        """
        Selecciona la caja preseleccionada.
        """
        self.slot_selected = self.selected_index
        self.show_menu = True  # Muestra el mini menú al lado de la caja seleccionada

        # Posicionar el mini menú a la derecha de la caja seleccionada, un poco más cerca y arriba
        slot_rect = self.slots[self.slot_selected].rect
        self.mini_menu.position = (slot_rect.right - 10, slot_rect.top - 10)  # Ajusta la posición según sea necesario
        self.mini_menu.rect.topleft = self.mini_menu.position

        print(f"MiniMenu position: {self.mini_menu.position}")  # Verificar posición
        self.mini_menu.show = True

    def deselect_slot(self):
        """
        Deselecciona la caja seleccionada y vuelve al modo de preselección.
        """
        self.slot_selected = None
        self.show_menu = False  # Oculta el mini menú
        self.update_preselection()

    def draw(self, screen):
        """
        Dibuja la pantalla del menú de Pokémon con los 6 slots.
        """
        draw_custom_background(screen)

        # Dibujar la imagen de la Pokébola
        pokeball_x = 20
        pokeball_y = 20
        screen.blit(self.pokeball_image, (pokeball_x, pokeball_y))

        # Dibujar el texto "EQUIPO POKÉMON"
        text_x = 100
        text_y = 10
        screen.blit(self.pokemon_text_surface, (text_x, text_y))

        # Dibujar los slots de Pokémon
        for slot in self.slots:
            slot.draw(screen)

        # Dibujar el Pokémon seleccionado en el centro-derecha de la pantalla
        if self.pokemon_team and self.selected_index < len(self.pokemon_team):
            selected_pokemon = self.pokemon_team[self.selected_index]
            if selected_pokemon.image:
                screen_width, screen_height = screen.get_size()
                max_image_size = (370, 370)
                pokemon_image = pygame.transform.scale(selected_pokemon.image, max_image_size)
                x_position = (screen_width - pokemon_image.get_width()) // 2 + 180
                y_position = (screen_height - pokemon_image.get_height()) // 2
                screen.blit(pokemon_image, (x_position, y_position))

            # Dibujar el mini menú si una caja está seleccionada
            # Dibujar el mini menú si una caja está seleccionada
            if self.show_menu and self.slot_selected is not None:
                self.mini_menu.draw(screen)

        # Dibujar el footer
        self.footer.draw(screen)

        pygame.display.flip()
