import pygame
import os
import game.utils as utils
import game.ui as ui
from game.dialogue_manager import DialogueManager, TextDisplayManager
from game.player import Player
from game.screen.choose_name_screen import ChooseNameScreen
from game.screen.main_menu_screen import MainMenuScreen
from game.sounds import SoundManager


class OakIntroScreen:
    def __init__(self):
        self.background_color = (255, 232, 127)
        self.profesor_oak = utils.load_image("../assets/img/oak_intro/profesor_oak.png", (350, 350))
        self.font = pygame.font.Font(utils.load_font(), 40)

        # Cargar imágenes y rectángulos de los Pokémon
        self.pokemons = {
            "Bulbasaur": (utils.load_image("../assets/pokemon_images/bulbasaur.png",
                                           (120, 120)), pygame.Rect(50, 280, 120, 120)),
            "Charmander": (utils.load_image("../assets/pokemon_images/charmander.png",
                                            (120, 120)), pygame.Rect(170, 280, 120, 120)),
            "Squirtle": (utils.load_image("../assets/pokemon_images/squirtle.png",
                                          (120, 120)), pygame.Rect(290, 280, 120, 120)),
        }

        self.selected_pokemon_name, self.selected_pokemon_type = "", ""  # Pokemon seleccionado
        self.starter_pokemon = False  # Pokemon confirmado

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
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("oak", loop=-1)

        # Text Display Manager para mostrar los diálogos carácter por carácter
        self.text_display_manager = TextDisplayManager(self.font)

        self.set_dialog_text()  # Abrimos con el primer bloque de dialogos

    def handle_events(self, event):
        """Maneja los eventos del teclado y mouse."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.handle_return_key()
            elif event.key == pygame.K_ESCAPE:
                return None
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if self.show_confirmation:
                    self.handle_confirmation_navigation(event.key)
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
                    # Asegurarse de que un Pokémon fue seleccionado antes de avanzar
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

    def handle_confirmation_navigation(self, key):
        """Maneja la navegación entre las opciones de confirmación (Sí/No)."""
        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.selected_confirmation_option = 'yes' if self.selected_confirmation_option == 'no' else 'no'

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
        """Retorna True si el bloque de dialogos se ha completado"""
        dialogues = self.dialogue_manager.get_dialogue(self.dialog_stage)
        if self.current_line_index >= len(dialogues) - 1:
            return True
        return False

    def handle_dialog_transition(self):
        """Controla la transición entre diferentes etapas del diálogo."""
        if self.dialog_stage == 'greeting':
            self.dialog_stage, self.current_line_index = 'name_prompt', 0
            return ChooseNameScreen(self)

        elif self.dialog_stage == 'name_prompt':
            self.current_line_index, self.dialog_stage, self.dialog_active = 0, 'info_starters', False

    def get_dialogue_with_placeholders(self, key, placeholders):
        """Obtiene el diálogo con los placeholders reemplazados."""
        return [utils.replace_placeholders(line, placeholders) for line in self.dialogue_manager.get_dialogue(key)]

    def set_dialog_text(self):
        if self.dialog_stage == 'select_starter':
            placeholders = {"pokemon_name": self.selected_pokemon_name, "pokemon_type": self.selected_pokemon_type}
            text = self.get_dialogue_with_placeholders('select_starter', placeholders)[self.current_line_index]
        elif self.dialog_stage == 'name_prompt':
            placeholders = {"player_name": self.player_name}
            text = self.get_dialogue_with_placeholders('name_prompt', placeholders)[self.current_line_index]
        else:
            text = self.dialogue_manager.get_dialogue(self.dialog_stage)[self.current_line_index]
        self.text_display_manager.set_text(text)

    def draw(self, screen):
        """Dibuja la pantalla de introducción."""
        screen.fill(self.background_color)
        screen.blit(self.profesor_oak, self.profesor_oak.get_rect(center=(self.oak_x, self.oak_y)))

        box_position = None

        if self.dialog_active:
            # Dibuja la caja de diálogo
            box_position = (10, 440)
            ui.draw_dialog_box(screen, position=box_position, border_color=(0, 0, 0),
                               fill_color=(255, 255, 255), border_thickness=5, border_radius=20)
            self.text_display_manager.draw(screen, box_position)

        if self.show_starters:
            if self.show_confirmation:
                # Solo dibujar el Pokémon seleccionado
                selected_pokemon_image, selected_pokemon_rect = self.pokemons[self.selected_pokemon_name]
                screen.blit(selected_pokemon_image, selected_pokemon_rect.topleft)
            else:
                # Dibujar todos los Pokémon si no se está confirmando
                for pokemon, (image, _) in self.pokemons.items():
                    screen.blit(image, self.pokemons[pokemon][1].topleft)

        if self.show_confirmation:
            # Caja de confirmación, colocada justo encima del cuadro de diálogo, alineada a la derecha con un margen
            # de 10px
            confirmation_box_width = 120
            confirmation_box_height = 140
            confirmation_box_x = screen.get_width() - confirmation_box_width - 10
            confirmation_box_y = box_position[1] - confirmation_box_height - 3

            # Dibuja el cuadro de confirmación con el mismo estilo que la caja de diálogo
            ui.draw_dialog_box(screen, position=(confirmation_box_x, confirmation_box_y),
                               box_width=confirmation_box_width, box_height=confirmation_box_height,
                               border_color=(0, 0, 0), fill_color=(255, 255, 255),
                               border_thickness=5, border_radius=20)

            # Texto "Yes" y "No"
            yes_no_font = pygame.font.Font(utils.load_font(), 35)
            yes_text = yes_no_font.render("Yes", True, (0, 0, 0))
            no_text = yes_no_font.render("No", True, (0, 0, 0))

            # Posiciones del texto "Yes" y "No"
            yes_text_pos = (confirmation_box_x + 40, confirmation_box_y + 30)
            no_text_pos = (confirmation_box_x + 40, confirmation_box_y + 80)

            screen.blit(yes_text, yes_text_pos)
            screen.blit(no_text, no_text_pos)

            # Dibuja la flecha ">" al lado de la opción seleccionada
            arrow_font = pygame.font.Font(utils.load_font(), 35)
            arrow_text = arrow_font.render(">", True, (0, 0, 0))

            # Mostrar la flecha a la izquierda de la opción seleccionada
            if self.selected_confirmation_option == 'yes':
                screen.blit(arrow_text, (yes_text_pos[0] - 20, yes_text_pos[1]))
            else:
                screen.blit(arrow_text, (no_text_pos[0] - 20, no_text_pos[1]))


