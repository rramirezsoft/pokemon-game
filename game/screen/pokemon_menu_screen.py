import pygame
from game.ui import PokemonSlot, Footer, MiniMenu, draw_pokemon_background, HealthBar
import game.utils as utils


class PokemonMenuScreen:
    def __init__(self, player, combat=None):
        """
        Inicializa la pantalla del menú de Pokémon con los 6 slots dispuestos en 1 columna.

        :param player: Objeto Player que contiene la información del jugador y sus Pokémon.
        """
        self.player = player
        self.combat = combat  # Instancia del combate (si la hay)
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
        self.pokemon_text_surface = self.font.render("POKÉMON TEAM", True, (0, 0, 0))

        # Crear el footer
        self.footer = Footer(text="Back")
        self.footer.footer_rect.topleft = (0, 575)

        #  Minimenu
        if self.combat:
            self.mini_menu = MiniMenu(position=(0, 0), size=(120, 100), options=["Data", "Switch", "Back"])
        else:
            self.mini_menu = MiniMenu(position=(0, 0), size=(120, 100), options=["Data", "Move", "Back"])

        self.moving_slot = None  # Variable para almacenar la primera caja seleccionada para mover.

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            # Si no estamos moviendo un Pokémon
            if self.moving_slot is None:
                if self.slot_selected is None:  # Solo permite mover la preselección si no hay selección activa
                    if event.key == pygame.K_DOWN:
                        # Mover preselección hacia abajo
                        next_index = (self.selected_index + 1) % len(self.slots)
                        # Verificar si el siguiente slot tiene un Pokémon, si no, no se mueve la selección
                        if 0 <= next_index < len(self.pokemon_team) and self.pokemon_team[next_index] is not None:
                            self.selected_index = next_index
                            self.update_preselection()

                    elif event.key == pygame.K_UP:
                        # Mover preselección hacia arriba
                        next_index = (self.selected_index - 1) % len(self.slots)
                        # Verificar si el slot anterior tiene un Pokémon, si no, no se mueve la selección
                        if 0 <= next_index < len(self.pokemon_team) and self.pokemon_team[next_index] is not None:
                            self.selected_index = next_index
                            self.update_preselection()

                    elif event.key == pygame.K_RETURN:
                        # Asegurarse de que el índice esté dentro del rango antes de acceder a pokemon_team
                        if 0 <= self.selected_index < len(self.pokemon_team):
                            # Seleccionar la caja preseleccionada solo si tiene un Pokémon
                            if self.pokemon_team[self.selected_index] is not None:
                                self.select_current_slot()
                            else:
                                print("No se puede seleccionar una caja vacía.")
                        else:
                            print("Índice fuera de rango.")

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        if self.slot_selected is not None:
                            # Deseleccionar la caja y ocultar el menú
                            self.deselect_slot()
                        else:
                            if self.combat:
                                return self.combat
                            from game.screen.main_menu_screen import MainMenuScreen
                            return MainMenuScreen(self.player)

                elif self.show_menu:
                    # Manejo de eventos para el mini menú
                    if event.key == pygame.K_DOWN:
                        # Mover la selección hacia abajo en el mini menú
                        self.mini_menu.selected_index = (self.mini_menu.selected_index + 1) % len(
                            self.mini_menu.options)

                    elif event.key == pygame.K_UP:
                        # Mover la selección hacia arriba en el mini menú
                        self.mini_menu.selected_index = (self.mini_menu.selected_index - 1) % len(
                            self.mini_menu.options)

                    elif event.key == pygame.K_RETURN:
                        # Ejecutar la opción seleccionada en el mini menú y cambiar de pantalla si es necesario
                        new_screen = self.execute_mini_menu_option()
                        if new_screen:
                            return new_screen

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        # Deseleccionar la caja y ocultar el mini menú
                        self.deselect_slot()

            # Si estamos en modo de movimiento de Pokémon
            else:
                if event.key == pygame.K_DOWN:
                    # Mover la preselección de destino hacia abajo
                    next_index = (self.selected_index + 1) % len(self.slots)
                    if 0 <= next_index < len(self.pokemon_team) and self.pokemon_team[next_index] is not None:
                        self.selected_index = next_index
                    self.update_preselection()  # Mostrar dos selecciones

                elif event.key == pygame.K_UP:
                    # Mover la preselección de destino hacia arriba
                    next_index = (self.selected_index - 1) % len(self.slots)
                    if 0 <= next_index < len(self.pokemon_team) and self.pokemon_team[next_index] is not None:
                        self.selected_index = next_index
                    self.update_preselection()  # Mostrar dos selecciones

                elif event.key == pygame.K_RETURN:
                    # Confirmar el intercambio de Pokémon entre las dos celdas seleccionadas
                    if (0 <= self.moving_slot < len(self.pokemon_team) and self.pokemon_team[
                        self.moving_slot] is not None and
                            0 <= self.selected_index < len(self.pokemon_team) and self.pokemon_team[
                                self.selected_index] is not None):
                        self.swap_pokemon_slots(self.moving_slot, self.selected_index)
                    else:
                        print("No se puede realizar el intercambio: asegúrate de que ambos slots contengan Pokémon.")
                    self.moving_slot = None  # Terminar el modo de movimiento
                    self.show_menu = False  # Ocultar el mini menú
                    self.slot_selected = None  # No hay caja seleccionada

                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    # Cancelar el modo de movimiento y volver a la preselección normal
                    self.moving_slot = None
                    self.update_preselection()  # Volver a la selección normal

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Detectar clic en una caja
            for index, slot in enumerate(self.slots):
                if slot.rect.collidepoint(mouse_pos):
                    if self.moving_slot is None:  # Si no hay movimiento activo
                        if self.slot_selected is None:  # Si no hay selección activa
                            # Si se hace clic en una caja, verificar si tiene un Pokémon
                            if 0 <= index < len(self.pokemon_team) and self.pokemon_team[index] is not None:
                                if index == self.selected_index:
                                    # Si se hace clic en la caja preseleccionada, seleccionarla
                                    self.select_current_slot()
                                else:
                                    # Si se hace clic en otra caja, preseleccionarla
                                    self.selected_index = index
                                    self.update_preselection()
                            else:
                                print("No se puede seleccionar una caja vacía.")

                        elif index == self.slot_selected:
                            # Si la caja seleccionada se clickea de nuevo, cerrar el menú
                            self.deselect_slot()
                    else:
                        # Si estamos en modo de movimiento, intercambiar Pokémon
                        if (0 <= self.moving_slot < len(self.pokemon_team) and self.pokemon_team[
                            self.moving_slot] is not None and
                                0 <= index < len(self.pokemon_team) and self.pokemon_team[index] is not None):
                            self.swap_pokemon_slots(self.moving_slot, index)
                        else:
                            print(
                                "No se puede realizar el intercambio: asegúrate de que ambos slots contengan Pokémon.")
                        self.moving_slot = None  # Terminar el modo de movimiento
                        self.show_menu = False  # Ocultar el mini menú

            # Manejo del clic en el mini menú
            if self.show_menu:
                option_index = self.mini_menu.is_option_clicked(event.pos)
                if option_index is not None:
                    self.mini_menu.selected_index = option_index
                    new_screen = self.execute_mini_menu_option()
                    if new_screen:
                        return new_screen

        # Manejo del evento del footer
        if self.footer.handle_events(event):
            if self.slot_selected is not None:
                # Deseleccionar la caja si está seleccionada
                self.deselect_slot()
            else:
                if self.combat:
                    return self.combat
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)

        return self

    def execute_mini_menu_option(self):
        """ Ejecuta la opción seleccionada en el mini menú. """
        option = self.mini_menu.options[self.mini_menu.selected_index]

        if option == "Back":
            self.deselect_slot()

        elif option == "Data":
            from game.screen.pokemon_data_screen import PokemonDataScreen
            if self.combat:
                return PokemonDataScreen(self.player, self.pokemon_team, self.selected_index, self.combat)
            return PokemonDataScreen(self.player, self.pokemon_team, self.selected_index)

        elif option == "Change Pokémon":
            # Aquí puedes añadir lógica futura para cambiar Pokémon en combate
            print("Opción de Cambiar Pokémon seleccionada (en combate, aún no implementada).")

        elif option == "Move":
            # Verificar si hay al menos dos Pokémon para intercambiar
            pokemon_count = sum(1 for pokemon in self.pokemon_team if pokemon is not None)
            if pokemon_count >= 2:
                # Iniciar el modo de movimiento
                self.moving_slot = self.selected_index
                self.show_menu = False  # Ocultar el mini menú mientras se realiza el movimiento
                print(f"Modo de movimiento iniciado con el slot: {self.moving_slot}")
            else:
                # Si no hay suficientes Pokémon para intercambiar, hacer lo mismo que "Atrás"
                self.deselect_slot()
                print("No hay suficientes Pokémon para mover, se vuelve al estado anterior.")

    def swap_pokemon_slots(self, slot_a, slot_b):
        """ Intercambia los Pokémon entre dos slots. """
        if slot_a is not None and slot_b is not None and slot_a != slot_b:
            # Intercambiar Pokémon
            pokemon_a = self.pokemon_team[slot_a]
            pokemon_b = self.pokemon_team[slot_b]

            if pokemon_a is not None and pokemon_b is not None:
                # Intercambiar Pokémon en el equipo
                self.pokemon_team[slot_a], self.pokemon_team[slot_b] = self.pokemon_team[slot_b], self.pokemon_team[
                    slot_a]

                # Actualizar las barras de salud
                self.slots[slot_a].pokemon = pokemon_b
                self.slots[slot_b].pokemon = pokemon_a

                # Re-inicializar las barras de salud
                self.slots[slot_a].health_bar = HealthBar(
                    pokemon_b.max_stats['hp'],
                    pokemon_b.current_hp,
                    self.slots[slot_a].health_bar.rect,
                    selected=self.slots[slot_a].selected
                )
                self.slots[slot_b].health_bar = HealthBar(
                    pokemon_a.max_stats['hp'],
                    pokemon_a.current_hp,
                    self.slots[slot_b].health_bar.rect,
                    selected=self.slots[slot_b].selected
                )

                # Restablecer la selección y salir del modo de movimiento
                self.moving_slot = None
                self.slot_selected = None
                self.show_menu = False

                # Actualizar la preselección
                self.update_preselection()
            else:
                self.moving_slot = None
                self.update_preselection()

    def update_preselection(self):
        """
        Actualiza la preselección de las cajas.
        Si estamos en modo de movimiento, destaca dos cajas: la de origen y la de destino.
        """
        for index, slot in enumerate(self.slots):
            if self.moving_slot is not None:
                # Si estamos en modo de movimiento, mostrar dos cajas seleccionadas
                slot.selected = (index == self.selected_index or index == self.moving_slot)
            else:
                # Si no estamos en modo de movimiento, solo se selecciona una caja
                slot.selected = (index == self.selected_index)

    def update(self):
        pass

    def select_current_slot(self):
        """
        Selecciona la caja preseleccionada.
        """
        if self.pokemon_team[self.selected_index] is not None:  # Solo seleccionar si el slot no está vacío
            self.slot_selected = self.selected_index
            self.show_menu = True  # Muestra el mini menú al lado de la caja seleccionada

            # Posicionar el mini menú a la derecha de la caja seleccionada
            slot_rect = self.slots[self.slot_selected].rect
            self.mini_menu.position = (
                slot_rect.right - 10, slot_rect.top - 10)  # Ajusta la posición según sea necesario
            self.mini_menu.rect.topleft = self.mini_menu.position

            print(f"MiniMenu position: {self.mini_menu.position}")  # Verificar posición
            self.mini_menu.show = True
        else:
            print("No se puede seleccionar una caja vacía.")

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
        screen_width, screen_height = screen.get_size()
        stripe_width = 100  # El ancho de la franja
        draw_pokemon_background(screen, [(0, 0), (screen_width // 2 + 130, 0), (0, screen_height + 450)],
                                [(screen_width // 2 + 130, 0),
                                 (screen_width // 2 + 130 + stripe_width, 0),
                                 (stripe_width, screen_height + 450), (0, screen_height + 450)],
                                (380, 220), (400, 400))

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
                max_image_size = (360, 360)
                pokemon_image = pygame.transform.scale(selected_pokemon.image, max_image_size)
                x_position = (screen_width - pokemon_image.get_width()) // 2 + 200
                y_position = (screen_height - pokemon_image.get_height()) // 2 + 50
                screen.blit(pokemon_image, (x_position, y_position))

            # Dibujar el mini menú si una caja está seleccionada
            # Dibujar el mini menú si una caja está seleccionada
            if self.show_menu and self.slot_selected is not None:
                self.mini_menu.draw(screen)

        # Dibujar el footer
        self.footer.draw(screen)

        pygame.display.flip()
