import pygame
import os
import game.utils as utils
import game.ui as ui
from game.dialogue_manager import DialogueManager
from game.player import Player
from game.pokemon import create_pokemon
from game.screen.main_menu_screen import MainMenuScreen


class OakIntroScreen:
    def __init__(self):
        self.background_color = (255, 232, 127)
        self.profesor_oak = utils.load_image("../assets/img/profesor_oak.png", (350, 350))
        self.font_path = utils.load_font()
        self.font = pygame.font.Font(self.font_path, 24)

        # Cargar las imágenes de los Pokémon iniciales
        self.bulbasaur = utils.load_image("../assets/pokemon_images/bulbasaur.png", (120, 120))
        self.charmander = utils.load_image("../assets/pokemon_images/charmander.png", (120, 120))
        self.squirtle = utils.load_image("../assets/pokemon_images/squirtle.png", (120, 120))

        # Rectángulos para detectar clics en los Pokémon
        self.bulbasaur_rect = self.bulbasaur.get_rect(topleft=(50, 280))
        self.charmander_rect = self.charmander.get_rect(topleft=(170, 280))
        self.squirtle_rect = self.squirtle.get_rect(topleft=(290, 280))

        # Pokémon seleccionado
        self.selected_pokemon = None
        self.selected_pokemon_name = ""
        self.selected_pokemon_type = ""

        # Construir la ruta absoluta al archivo JSON
        base_path = os.path.dirname(__file__)
        json_path = os.path.join(base_path, '..', 'data', 'dialogues.json')
        self.dialogue_manager = DialogueManager(os.path.abspath(json_path))
        self.dialogue_manager.set_context('professor')

        # Variables para el manejo de dialogos.
        self.current_line_index = 0
        self.dialog_active = True
        self.getting_name = False
        self.player_name = ""
        self.dialog_stage = 'greeting'
        self.player = None

        # Inicializar variables para el movimiento de Oak
        self.oak_x = 400
        self.oak_y = 250
        self.oak_target_x = 500
        self.oak_speed = 2
        self.show_starters = False

    def handle_events(self, event):
        """Maneja los eventos del teclado y mouse."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if (self.dialog_stage == 'greeting' or self.dialog_stage ==
                        'name_prompt' or self.dialog_stage == 'info_starters'):
                    self.next_line()
                elif self.dialog_stage == 'name_input' and self.player_name:
                    self.dialog_stage = 'name_prompt'
                    self.current_line_index = 0
                    self.player = Player(self.player_name)
                elif self.dialog_stage == 'select_starter':
                    starter_pokemon = create_pokemon(self.selected_pokemon_name)
                    if starter_pokemon:
                        self.player.get_starter(starter_pokemon)
                        print(self.player.__str__())

                    self.dialog_stage = 'confirm_starter'
                    self.current_line_index = 0
                elif self.dialog_stage == 'confirm_starter':

                    return MainMenuScreen()
            elif event.key == pygame.K_BACKSPACE and self.dialog_stage == 'name_input':
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_ESCAPE:
                return None
            else:
                if self.dialog_stage == 'name_input':
                    char = event.unicode
                    if char.isalnum() or char in [' ', '_']:
                        self.player_name += char

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Detecta si el usuario hace clic en uno de los Pokémon
            mouse_pos = event.pos
            if self.show_starters:
                if self.bulbasaur_rect.collidepoint(mouse_pos):
                    self.select_pokemon("Bulbasaur", "Planta")
                elif self.charmander_rect.collidepoint(mouse_pos):
                    self.select_pokemon("Charmander", "Fuego")
                elif self.squirtle_rect.collidepoint(mouse_pos):
                    self.select_pokemon("Squirtle", "Agua")
        return self

    def select_pokemon(self, name, pokemon_type):
        """Selecciona un Pokémon y muestra el diálogo correspondiente."""
        self.selected_pokemon_name = name
        self.selected_pokemon_type = pokemon_type
        self.dialog_stage = 'select_starter'
        self.current_line_index = 0
        self.dialog_active = True

    def update(self):
        # Mover a Oak solo si aún no ha llegado al objetivo y el diálogo no está activo
        if not self.dialog_active and self.oak_x < self.oak_target_x:
            self.oak_x += self.oak_speed
        elif self.oak_x >= self.oak_target_x and not self.dialog_active:

            self.oak_x = self.oak_target_x
            self.dialog_active = True
            self.dialog_stage = 'info_starters'
            self.current_line_index = 0
            self.show_starters = True

    def next_line(self):
        """Avanza a la siguiente línea del diálogo o al siguiente diálogo."""
        if self.dialog_stage == 'greeting':
            dialogues = self.dialogue_manager.get_dialogue('greeting')
            if self.current_line_index < len(dialogues) - 1:
                self.current_line_index += 1
            else:
                self.dialog_stage = 'name_input'
                self.current_line_index = 0
        elif self.dialog_stage == 'name_prompt':
            dialogues = self.dialogue_manager.get_dialogue('name_prompt')
            if self.current_line_index < len(dialogues) - 1:
                self.current_line_index += 1
            else:
                self.dialog_stage = 'info_starters'
                self.dialog_active = False  # Detener el diálogo temporalmente hasta que Oak llegue a su destino
        elif self.dialog_stage == 'info_starters':
            dialogues = self.dialogue_manager.get_dialogue('info_starters')
            if self.current_line_index < len(dialogues) - 1:
                self.current_line_index += 1

    def get_dialogue_with_placeholders(self, key, placeholders):
        """Obtiene el diálogo con los placeholders reemplazados."""
        dialogues = self.dialogue_manager.get_dialogue(key)
        return [utils.replace_placeholders(line, placeholders) for line in dialogues]

    def draw(self, screen):
        # Rellenar el fondo con el color de fondo
        screen.fill(self.background_color)

        # Dibujar al profesor Oak
        oak_rect = self.profesor_oak.get_rect(center=(self.oak_x, self.oak_y))
        screen.blit(self.profesor_oak, oak_rect)

        if self.dialog_active:
            box_position = (10, 440)

            ui.draw_dialog_box(
                screen,
                position=box_position,
                border_color=(0, 0, 0),
                fill_color=(255, 255, 255),
                border_thickness=5,
                border_radius=20
            )

            if self.dialog_stage == 'name_input':

                # Mostrar el nombre ingresado hasta ahora
                name_text = "Escribe tu nombre: " + self.player_name
                ui.draw_text_in_dialog_box(
                    screen,
                    text=name_text,
                    font=self.font,
                    position=(box_position[0], box_position[1]),  # Posición ajustada para el nombre
                )
            elif self.dialog_stage == 'name_prompt':
                # Obtener el texto actual del diálogo con el nombre del jugador
                dialogues = self.get_dialogue_with_placeholders('name_prompt', {"player_name": self.player_name})
                current_text = dialogues[self.current_line_index]

                # Dibujar el texto dentro del bocadillo
                ui.draw_text_in_dialog_box(
                    screen,
                    text=current_text,
                    font=self.font,
                    position=box_position,
                )
            elif self.dialog_stage == 'select_starter':
                # Obtener el diálogo de selección del Pokémon
                placeholders = {
                    "pokemon_name": self.selected_pokemon_name,
                    "pokemon_type": self.selected_pokemon_type
                }
                dialogues = self.get_dialogue_with_placeholders('select_starter', placeholders)
                current_text = dialogues[self.current_line_index]

                # Dibujar el diálogo del Pokémon seleccionado
                ui.draw_text_in_dialog_box(
                    screen,
                    text=current_text,
                    font=self.font,
                    position=box_position,
                )
            else:
                # Obtener el texto actual del diálogo
                dialogues = self.dialogue_manager.get_dialogue(self.dialog_stage)
                current_text = dialogues[self.current_line_index]

                # Dibujar el texto dentro del bocadillo
                ui.draw_text_in_dialog_box(
                    screen,
                    text=current_text,
                    font=self.font,
                    position=box_position,
                )

            # Mostrar las imágenes de los Pokémon iniciales si es el momento adecuado
            if self.show_starters:
                screen.blit(self.bulbasaur, (50, 280))  # Posición de Bulbasaur
                screen.blit(self.charmander, (170, 280))  # Posición de Charmander
                screen.blit(self.squirtle, (290, 280))  # Posición de Squirtle
