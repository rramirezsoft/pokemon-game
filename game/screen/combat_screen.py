import os
import pygame
from game import utils
import game.ui as ui
from game.combat import Combat
from game.dialogue_manager import TextDisplayManager, DialogueManager


class CombatScreen:
    def __init__(self, player, enemy_pokemon):
        """Inicializa la pantalla de combate."""
        self.player = player
        self.enemy_pokemon = enemy_pokemon
        self.font = pygame.font.Font(utils.load_font(), 40)
        self.background_color = (232, 210, 224)

        self.combat = Combat(self.player, enemy_pokemon)  # Iniciamos el combate
        self.player_current_pokemon = self.combat.current_pokemon

        # Sistema de diálogos
        self.dialogue_manager = DialogueManager(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'dialogues.json'))
        )
        self.text_display_manager = TextDisplayManager(self.font)
        self.dialogue_manager.set_context("combat")
        self.dialogue_stage = "encounter"

        # Diálogos iniciales con placeholders
        self.dialogue_lines = self.dialogue_manager.get_dialogue_with_placeholders(
            "encounter", {"enemy_pokemon": self.enemy_pokemon.name, "player_pokemon": self.player_current_pokemon.name}
        )
        self.current_dialogue_index = 0
        self.current_dialogue = self.dialogue_lines[self.current_dialogue_index]

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load("../assets/img/battle/campo_batalla.png").convert_alpha()
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.background_image = utils.resize_image_to_width(self.background_image, self.screen_width)

        self.pokeball_image = utils.load_image("../assets/img/icons/pokeball.png", (20, 20))

        # Configurar movimientos de los Pokémon usando MovementManager
        self.player_pokemon_movement = ui.PokemonCombatMovement(
            start_pos=(-300, 260),
            end_pos=(100, 265),
            callback_on_complete=self.on_player_pokemon_moved
        )
        self.enemy_pokemon_movement = ui.PokemonCombatMovement(
            start_pos=(-200, 92),
            end_pos=(500, 92),
            callback_on_complete=self.on_enemy_pokemon_moved
        )

        # Configurar movimientos de las cajas de estado
        self.player_box_movement = ui.PokemonCombatMovement(
            start_pos=(self.screen_width, 300),
            end_pos=(self.screen_height - 51, 300),
        )
        self.enemy_box_movement = ui.PokemonCombatMovement(
            start_pos=(-250, 50),
            end_pos=(2, 50),
        )

        # Flags
        self.enemy_moved = False
        self.player_pokemon_moved = False
        self.waiting_for_move_player_pokemon = True
        self.action_stage = False  # Estado del menú de opciones

        self.option_rects = []  # Inicialización de los rectángulos del menú de acciones

        # Escala para las imágenes de los Pokémon
        self.player_pokemon_scale_factor = 0.6
        self.enemy_pokemon_scale_factor = 0.4

        self.combat_over = False  # Estado del combate (en curso/terminado)

    def change_stage(self, new_stage, placeholders=None):
        """Cambia el estado del combate y actualiza los diálogos."""
        placeholders = placeholders or {}
        self.dialogue_stage = new_stage
        self.dialogue_lines = self.dialogue_manager.get_dialogue_with_placeholders(new_stage, placeholders)
        self.current_dialogue_index = 0
        self.current_dialogue = self.dialogue_lines[self.current_dialogue_index]
        self.text_display_manager.set_text(self.current_dialogue)

        # Si el nuevo estado requiere el menú de acciones
        if new_stage == "actions":
            self.action_stage = True
        else:
            self.action_stage = False

    def on_enemy_pokemon_moved(self):
        """Callback cuando el Pokémon enemigo completa su movimiento."""
        self.enemy_moved = True
        self.text_display_manager.set_text(self.current_dialogue)

    def on_player_pokemon_moved(self):
        """Callback cuando el Pokémon del jugador completa su movimiento."""
        self.player_pokemon_moved = True

    def handle_events(self, event):
        """Maneja los eventos de la pantalla de combate."""
        if self.text_display_manager.is_dialogue_complete():
            # Verificar si se presionó la tecla "Enter" para avanzar el diálogo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if not self.enemy_moved:
                    return self
                else:
                    # Avanzar al siguiente diálogo si el texto ya ha sido mostrado completamente
                    if self.current_dialogue_index < len(self.dialogue_lines) - 1:
                        self.current_dialogue_index += 1
                        self.current_dialogue = self.dialogue_lines[self.current_dialogue_index]
                        self.text_display_manager.set_text(self.current_dialogue)

                        # Activar el movimiento del Pokémon del jugador al mostrar el segundo diálogo
                        if self.dialogue_stage == 'encounter' and self.current_dialogue_index == 1:
                            self.waiting_for_move_player_pokemon = False
                    else:
                        # Cambiar a la etapa de acciones cuando termine el diálogo inicial
                        if self.dialogue_stage == "encounter" and self.player_pokemon_moved:
                            self.change_stage("actions", {"player_pokemon": self.player_current_pokemon.name})

                # Verificar si estamos en el estado 'escaped' y el jugador presionó Enter
                if self.dialogue_stage == "escaped":
                    self.combat_over = True
                    from game.screen.main_menu_screen import MainMenuScreen
                    return MainMenuScreen(self.player)

            # Si el menú de acciones está activo puedes clickar en las cajas
            if event.type == pygame.MOUSEBUTTONDOWN and self.action_stage:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            print("Fight")
                        elif i == 1:
                            print("Bag")
                        elif i == 2:
                            from game.screen.pokemon_menu_screen import PokemonMenuScreen
                            return PokemonMenuScreen(self.player, self)
                        elif i == 3:
                            escaped = self.combat.attempt_escape()
                            if escaped:
                                self.change_stage("escaped")
                            else:
                                self.change_stage("failed_escape")

        return self

    def update(self):
        """Actualiza el estado de la pantalla de combate."""
        self.enemy_pokemon_movement.update()
        if self.enemy_moved:
            self.enemy_box_movement.update()

        if self.enemy_moved and not self.waiting_for_move_player_pokemon:
            self.player_pokemon_movement.update()
        if self.player_pokemon_moved:
            self.player_box_movement.update()

        # Actualizar el sistema de diálogo
        self.text_display_manager.update()

    def draw(self, screen):
        """Dibuja la pantalla de combate."""
        screen.blit(self.background_image, (0, 0))

        # Dibujar el Pokémon del jugador si ya se ha movido
        utils.draw_pokemon(screen, self.player_current_pokemon, self.player_pokemon_movement.get_position(),
                           self.player_pokemon_scale_factor)
        ui.draw_combat_background(screen)

        # Dibujar el Pokémon enemigo
        utils.draw_pokemon(screen, self.enemy_pokemon,
                           self.enemy_pokemon_movement.get_position(), self.enemy_pokemon_scale_factor)

        # Dibujar las cajas de estado cuando lleguen a su posición
        if self.enemy_moved:
            ui.draw_combat_pokemon_status_box(screen, self.enemy_pokemon, self.enemy_box_movement.get_position(),
                                              is_player_pokemon=False, player=self.player,
                                              pokeball_image=self.pokeball_image)

        if self.player_pokemon_moved:
            ui.draw_combat_pokemon_status_box(screen, self.player_current_pokemon,
                                              self.player_box_movement.get_position(), is_player_pokemon=True)

        # Dibujar el recuadro para el texto y mostrar el texto dentro
        if self.action_stage:
            dialog_box_width = 400
            self.option_rects = ui.draw_action_menu(screen, pygame.mouse.get_pos())
        else:
            dialog_box_width = 792
        ui.draw_dialog_box(screen, box_width=dialog_box_width)
        self.text_display_manager.draw(screen)
