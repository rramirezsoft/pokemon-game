import pygame
import os
from game import utils, ui
from game.dialogue_manager import DialogueManager, TextDisplayManager
from game.player import Player
from game.screen.base_screen import BaseScreen
from game.screen.main_menu_screen import MainMenuScreen


class OakIntroScreen(BaseScreen):
    def __init__(self):
        super().__init__(None)
        self.background_color = (255, 232, 127)
        self.profesor_oak = utils.load_image("../assets/img/oak_intro/profesor_oak.png", (350, 350))
        self.font = pygame.font.Font(utils.load_font(), 40)

        # Cargar imágenes y rectángulos de los Pokémon
        self.pokemons = {
            "Bulbasaur": (
            utils.load_image("../assets/pokemon_images/bulbasaur.png", (120, 120)), pygame.Rect(50, 280, 120, 120)),
            "Charmander": (
            utils.load_image("../assets/pokemon_images/charmander.png", (120, 120)), pygame.Rect(170, 280, 120, 120)),
            "Squirtle": (
            utils.load_image("../assets/pokemon_images/squirtle.png", (120, 120)), pygame.Rect(290, 280, 120, 120)),
        }

        self.selected_pokemon_name, self.selected_pokemon_type = "", ""
        self.starter_pokemon = False

        # Diálogos
        self.dialogue_manager = DialogueManager(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'dialogues.json'))
        )
        self.dialogue_manager.set_context('professor')
        self.dialog_stage = 'greeting'
        self.current_line_index = 0
        self.dialog_active = True

        self.player_name = ""
        self.player = None

        self.show_starters = False
        self.show_confirmation = False
        self.selected_confirmation_option = "no"

        # Movimiento de Oak
        self.oak_x, self.oak_y, self.oak_target_x = 400, 250, 500
        self.oak_speed = 2

        # Música
        self.sound_manager.play_music("oak", loop=-1)

        self.text_display_manager = TextDisplayManager(self.font)

        self.set_dialog_text()  # Abrimos con el primer bloque de diálogos

    def handle_events(self, event):
        """Maneja los eventos del teclado y mouse."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.handle_return_key()
            elif event.key == pygame.K_ESCAPE:
                return None
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                if self.show_confirmation:
                    self.selected_confirmation_option = utils.handle_confirmation_navigation(
                        self.selected_confirmation_option, event.key
                    )
        elif (event.type == pygame.MOUSEBUTTONDOWN and self.show_starters
              and not self.show_confirmation and self.text_display_manager.is_dialogue_complete()):
            self.handle_mouse_click(event.pos)
        return self

    def handle_return_key(self):
        """Maneja la lógica cuando se presiona Enter."""
        if self.text_display_manager.is_dialogue_complete():
            if self.show_confirmation:
                if self.selected_confirmation_option == 'yes':
                    self.starter_pokemon = True
                    self.player = Player(self.player_name)
                    self.player.get_starter(self.selected_pokemon_name)
                    self.dialog_stage = 'confirm_starter'
                elif self.selected_confirmation_option == 'no':
                    self.dialog_stage = 'info_starters'
                    self.current_line_index = 1
                self.set_dialog_text()
                self.show_confirmation = False
            else:
                if self.dialog_stage == 'greeting' and self.is_block_complete():
                    self.current_line_index = 0
                    self.dialog_stage = 'name_prompt'
                    return ChooseNameScreen(self)
                # Si el texto ya está completo, avanzamos al siguiente diálogo.
                if self.dialog_stage in ['greeting', 'name_prompt', 'info_starters']:
                    self.next_line()
                elif self.dialog_stage == 'select_starter' and self.selected_pokemon_name:
                    self.show_confirmation = True
                if self.dialog_stage == 'confirm_starter':
                    self.sound_manager.stop_music()
                    return MainMenuScreen(self.player)

        return self

    def handle_mouse_click(self, mouse_pos):
        """Detecta si el usuario ha hecho clic en uno de los Pokémon iniciales."""
        if not self.starter_pokemon:
            for name, (_, rect) in self.pokemons.items():
                if rect.collidepoint(mouse_pos):
                    self.select_pokemon(name, {"Bulbasaur": "Grass-type",
                                               "Charmander": "Fire-type", "Squirtle": "Water-type"}[name])

    def select_pokemon(self, name, pokemon_type):
        """Selecciona un Pokémon y actualiza el estado de diálogo."""
        self.selected_pokemon_name, self.selected_pokemon_type = name, pokemon_type
        self.dialog_stage, self.current_line_index, self.dialog_active = 'select_starter', 0, True
        self.show_confirmation = True  # Para mostrar el cuadro de confirmación
        self.selected_confirmation_option = 'no'
        self.set_dialog_text()  # Actualiza el texto al seleccionar el Pokémon

    def update(self):
        """Actualiza el movimiento de Oak."""
        if not self.dialog_active and self.oak_x < self.oak_target_x:
            self.oak_x += self.oak_speed
        elif self.oak_x >= self.oak_target_x and not self.dialog_active:
            self.oak_x, self.dialog_active, self.dialog_stage = self.oak_target_x, True, 'info_starters'
            self.current_line_index, self.show_starters = 0, True
        # Actualiza el texto mostrado en el TextDisplayManager
        if self.dialog_active:
            self.text_display_manager.update()

    def next_line(self):
        """Avanza a la siguiente línea de diálogo o al siguiente diálogo."""
        dialogues = self.dialogue_manager.get_dialogue(self.dialog_stage)
        if self.current_line_index < len(dialogues) - 1:
            self.current_line_index += 1
        else:
            self.handle_dialog_transition()
        self.set_dialog_text()

    def is_block_complete(self):
        """Retorna True si el bloque de diálogos se ha completado."""
        dialogues = self.dialogue_manager.get_dialogue(self.dialog_stage)
        return self.current_line_index >= len(dialogues) - 1

    def handle_dialog_transition(self):
        """Controla la transición entre diferentes etapas del diálogo."""
        if self.dialog_stage == 'greeting':
            self.dialog_stage, self.current_line_index = 'name_prompt', 0
            return ChooseNameScreen(self)

        elif self.dialog_stage == 'name_prompt':
            self.current_line_index, self.dialog_stage, self.dialog_active = 0, 'info_starters', False

    def set_dialog_text(self):
        """Configura el texto actual del diálogo."""
        if self.dialog_stage == 'select_starter':
            placeholders = {"pokemon_name": self.selected_pokemon_name, "pokemon_type": self.selected_pokemon_type}
            text = self.dialogue_manager.get_dialogue_with_placeholders('select_starter',
                                                                        placeholders)[self.current_line_index]
        elif self.dialog_stage == 'name_prompt':
            placeholders = {"player_name": self.player_name}
            text = self.dialogue_manager.get_dialogue_with_placeholders('name_prompt', placeholders
                                                                        )[self.current_line_index]
        else:
            text = self.dialogue_manager.get_dialogue(self.dialog_stage)[self.current_line_index]
        self.text_display_manager.set_text(text)

    def draw(self, screen):
        """Dibuja la pantalla de introducción."""
        screen.fill(self.background_color)
        screen.blit(self.profesor_oak, self.profesor_oak.get_rect(center=(self.oak_x, self.oak_y)))

        box_position = None

        if self.dialog_active:
            box_position = (4, 449)
            ui.draw_dialog_box(screen)
            self.text_display_manager.draw(screen)

        if self.show_starters:
            if self.show_confirmation:
                selected_pokemon_image, selected_pokemon_rect = self.pokemons[self.selected_pokemon_name]
                screen.blit(selected_pokemon_image, selected_pokemon_rect.topleft)
            else:
                for pokemon, (image, _) in self.pokemons.items():
                    screen.blit(image, self.pokemons[pokemon][1].topleft)

        if self.show_confirmation:
            confirmation_box_position = (screen.get_width() - 145, box_position[1] - 140)
            utils.draw_confirmation_box(screen, self.selected_confirmation_option,
                                        position=confirmation_box_position)

        pygame.display.flip()


class ChooseNameScreen:
    def __init__(self, oak_intro_screen):
        self.oak_intro_screen = oak_intro_screen
        self.background_color = (255, 232, 127)
        self.font = pygame.font.Font(utils.load_font(), 40)
        self.font_large = pygame.font.Font(utils.load_font(), 60)

        # Parámetros del nombre
        self.max_name_length = 10
        self.current_name = ""

        # Tamaño de la pantalla
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        # Botones del teclado
        self.buttons = []
        self.create_keyboard_buttons()

        # Colores y sombras para la UI
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)
        self.text_color = (0, 0, 0)
        self.box_color = (255, 255, 255)
        self.container_color = (230, 164, 62)
        self.button_container_color = (250, 186, 88)

    def create_keyboard_buttons(self):
        """Crea los botones del teclado con letras y símbolos."""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        button_width, button_height = 60, 60
        padding = 10

        # Botones de confirmación y borrar estilizados
        total_width_action_buttons = 300 + padding
        x_action_start = (self.screen_width - total_width_action_buttons) // 2

        self.buttons.append(('DEL', pygame.Rect(x_action_start, 160, 130, 60)))
        self.buttons.append(('OK', pygame.Rect(x_action_start + 130 + padding, 160, 130, 60)))

        # Centramos el teclado horizontalmente y ajustamos su posición vertical más cerca de los botones "DEL" y "OK"
        total_keyboard_width = (button_width + padding) * 7 - padding
        x_start = (self.screen_width - total_keyboard_width) // 2
        y_start = 250

        for i, letter in enumerate(letters):
            x = x_start + (i % 7) * (button_width + padding)  # Distribuir 7 letras por fila
            y = y_start + (i // 7) * (button_height + padding)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append((letter, rect))

    def handle_events(self, event):
        """Maneja los eventos del mouse y teclado."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for letter, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return self.handle_button_click(letter)
        return self

    def handle_button_click(self, letter):
        """Acciones cuando se presiona un botón."""
        if letter == 'DEL':
            self.current_name = self.current_name[:-1]
        elif letter == 'OK' and self.current_name:
            # Confirma el nombre y vuelve a OakIntroScreen
            self.oak_intro_screen.player_name = self.current_name
            self.oak_intro_screen.set_dialog_text()
            return self.oak_intro_screen  # Regresa a la pantalla de Oak
        elif len(self.current_name) < self.max_name_length:
            self.current_name += letter
        return self  # Devolver la pantalla actual después de la acción

    def draw(self, screen):
        """Dibuja la pantalla de selección de nombre."""
        screen.fill(self.background_color)

        # Contenedor alrededor de la caja de texto y los botones
        container_width = 640
        container_height = 520
        container_rect = pygame.Rect((self.screen_width - container_width) // 2, 30, container_width, container_height)
        pygame.draw.rect(screen, self.container_color, container_rect, border_radius=15)

        # Caja de texto con el nombre actual centrada, con guiones bajos para letras faltantes
        name_box_width = 600
        name_box_height = 80
        name_box_rect = pygame.Rect((self.screen_width - name_box_width) // 2, 50, name_box_width, name_box_height)
        pygame.draw.rect(screen, self.box_color, name_box_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), name_box_rect, 3, border_radius=10)

        # Contenedor alrededor de los botones
        button_container_width = 550
        button_container_height = 390
        button_container_rect = pygame.Rect((self.screen_width - button_container_width) // 2, 145,
                                            button_container_width, button_container_height)
        pygame.draw.rect(screen, self.button_container_color, button_container_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_container_rect, 3,
                         border_radius=10)

        char_spacing = 40  # Espacio entre los caracteres
        start_x = (self.screen_width - (char_spacing * self.max_name_length)) // 2

        for i in range(self.max_name_length):
            char = self.current_name[i] if i < len(self.current_name) else '_'
            char_surface = self.font_large.render(char, True, self.text_color)

            # Posiciona los caracteres (letras o guiones bajos) de forma centrada
            char_x = start_x + char_spacing * i
            char_y = name_box_rect.y + (name_box_height - char_surface.get_height()) // 2

            screen.blit(char_surface, (char_x, char_y))

        # Dibuja los botones de "DEL" y "OK" justo debajo del cuadro del nombre
        for letter, rect in self.buttons:
            color = self.button_color
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = self.button_hover_color
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=10)

            # Dibuja el texto sobre cada botón
            text_surf = self.font.render(letter, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                                    rect.y + (rect.height - text_surf.get_height()) // 2))

        pygame.display.flip()

    def update(self):
        """Actualiza el estado de la pantalla."""
        pass
