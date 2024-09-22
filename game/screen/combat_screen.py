import os
import pygame
from game import utils
import game.ui as ui
from game.dialogue_manager import TextDisplayManager, DialogueManager


class CombatScreen:
    def __init__(self, player, enemy_pokemon):
        """Inicializa la pantalla de combate."""
        self.player = player
        self.player_current_pokemon = player.pokemons[0]
        self.enemy_pokemon = enemy_pokemon
        self.font = pygame.font.Font(utils.load_font(), 40)
        self.background_color = (232, 210, 224)

        # Sistema de diálogos
        self.dialogue_manager = DialogueManager(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'dialogues.json'))
        )
        self.text_display_manager = TextDisplayManager(self.font)
        self.dialogue_manager.set_context("combat")
        self.dialogue_stage = "encounter"

        # Diálogos con placeholders
        self.dialogue_lines = self.dialogue_manager.get_dialogue_with_placeholders(
            "encounter",  # Clave del diálogo
            {
                "enemy_pokemon": self.enemy_pokemon.name,
                "player_pokemon": self.player_current_pokemon.name
            }
        )
        self.current_dialogue_index = 0
        self.current_dialogue = self.dialogue_lines[self.current_dialogue_index]

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load("../assets/img/battle/campo_batalla.png").convert_alpha()
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.background_image = utils.resize_image_to_width(self.background_image, self.screen_width)

        self.pokeball_image = utils.load_image("../assets/img/icons/pokeball.png", (20, 20))

        # Inicializar las posiciones de los Pokémon
        self.player_pokemon_pos = (-300, 260)
        self.enemy_pokemon_start_pos = (-200, 92)
        self.enemy_pokemon_end_pos = (500, 92)
        self.player_pokemon_end_pos = (100, 265)

        # Configurar la animación de movimiento
        self.pokemon_speed = 8
        self.enemy_pokemon_current_pos = list(self.enemy_pokemon_start_pos)
        self.player_pokemon_current_pos = list(self.player_pokemon_pos)

        # Posiciones iniciales y finales para las cajas de estado
        self.player_box_start_pos = (self.screen_width, 300)
        self.enemy_box_start_pos = (-250, 50)
        self.player_box_end_pos = (self.screen_height - 51, 300)
        self.enemy_box_end_pos = (2, 50)

        self.enemy_box_current_pos = list(self.enemy_box_start_pos)
        self.player_box_current_pos = list(self.player_box_start_pos)

        # Estado de las animaciones
        self.enemy_moved = False
        self.player_moved = False
        self.waiting_for_next_dialogue = True

        # Escala para las imágenes de los Pokémon
        self.player_pokemon_scale_factor = 0.6
        self.enemy_pokemon_scale_factor = 0.4

    def handle_events(self, event):
        """Maneja los eventos de la pantalla de combate."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not self.text_display_manager.is_dialogue_complete():
                print("Aun no ha acabado este dialogo")
            else:
                # Avanzar al siguiente diálogo si el texto ya ha sido mostrado completamente
                if self.current_dialogue_index < len(self.dialogue_lines) - 1:
                    self.current_dialogue_index += 1
                    self.current_dialogue = self.dialogue_lines[self.current_dialogue_index]
                    self.text_display_manager.set_text(self.current_dialogue)

                    # Activar el movimiento del Pokémon del jugador al mostrar el segundo diálogo
                    if self.current_dialogue_index == 1:
                        self.waiting_for_next_dialogue = False  # Permitir que el Pokémon del jugador se mueva
        return self

    def update(self):
        """Actualiza el estado de la pantalla de combate."""
        # Mover el Pokémon enemigo hacia su posición final
        if self.enemy_pokemon_current_pos[0] < self.enemy_pokemon_end_pos[0]:
            self.enemy_pokemon_current_pos[0] += self.pokemon_speed
            if self.enemy_pokemon_current_pos[0] >= self.enemy_pokemon_end_pos[0]:
                self.enemy_pokemon_current_pos[0] = self.enemy_pokemon_end_pos[0]
                self.text_display_manager.set_text(self.current_dialogue)
                self.enemy_moved = True

        # Si el enemigo ha llegado, mover su caja de estado
        if self.enemy_moved and self.enemy_box_current_pos[0] < self.enemy_box_end_pos[0]:
            self.enemy_box_current_pos[0] += self.pokemon_speed
            if self.enemy_box_current_pos[0] >= self.enemy_box_end_pos[0]:
                self.enemy_box_current_pos[0] = self.enemy_box_end_pos[0]

        # Mover el Pokémon del jugador después de que el enemigo haya terminado y cuando el diálogo avance
        if self.enemy_moved and not self.waiting_for_next_dialogue:
            if self.player_pokemon_current_pos[0] < self.player_pokemon_end_pos[0]:
                self.player_pokemon_current_pos[0] += self.pokemon_speed
                if self.player_pokemon_current_pos[0] >= self.player_pokemon_end_pos[0]:
                    self.player_pokemon_current_pos[0] = self.player_pokemon_end_pos[0]
                    self.player_moved = True

        # Si el jugador ha llegado, mover su caja de estado
        if self.player_moved and self.player_box_current_pos[0] > self.player_box_end_pos[0]:
            self.player_box_current_pos[0] -= self.pokemon_speed
            if self.player_box_current_pos[0] <= self.player_box_end_pos[0]:
                self.player_box_current_pos[0] = self.player_box_end_pos[0]

        # Actualizar el sistema de diálogo
        self.text_display_manager.update()

    def draw(self, screen):
        """Dibuja la pantalla de combate."""
        screen.blit(self.background_image, (0, 0))

        # Dibujar el Pokémon del jugador si ya se ha movido
        utils.draw_pokemon(screen, self.player_current_pokemon, self.player_pokemon_current_pos,
                           self.player_pokemon_scale_factor)
        ui.draw_combat_background(screen)

        # Dibujar el Pokémon enemigo
        utils.draw_pokemon(screen, self.enemy_pokemon, self.enemy_pokemon_current_pos, self.enemy_pokemon_scale_factor)

        # Dibujar las cajas de estado cuando lleguen a su posición
        if self.enemy_moved:
            ui.draw_combat_pokemon_status_box(screen, self.enemy_pokemon, self.enemy_box_current_pos,
                                              is_player_pokemon=False, player=self.player,
                                              pokeball_image=self.pokeball_image)

        if self.player_moved:
            ui.draw_combat_pokemon_status_box(screen, self.player_current_pokemon, self.player_box_current_pos,
                                              is_player_pokemon=True)

        # Dibujar el recuadro para el texto
        ui.draw_dialog_box(screen)

        # Mostrar el texto de diálogo actual
        self.text_display_manager.draw(screen)
