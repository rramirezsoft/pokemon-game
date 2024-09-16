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
        self.encounter_text = (
            self.dialogue_manager.get_dialogue(self.dialogue_stage).format(pokemon_enemy=self.enemy_pokemon.name))

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load("../assets/img/battle/campo_batalla.png").convert_alpha()
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.background_image = self.resize_image_to_width(self.background_image, self.screen_width)

        # Inicializar las posiciones de los Pokémon
        self.player_pokemon_pos = (100, 260)
        self.enemy_pokemon_start_pos = (-200, 92)  # Inicio fuera de la pantalla (lado izquierdo)
        self.enemy_pokemon_end_pos = (500, 92)  # Posición final del Pokémon enemigo (lado derecho)

        # Configurar la animación de movimiento del enemigo
        self.pokemon_speed = 6  # Velocidad de movimiento del enemigo
        self.enemy_pokemon_current_pos = list(self.enemy_pokemon_start_pos)

        # Factor de escala para las imágenes de los Pokémon
        self.player_pokemon_scale_factor = 0.6  # Escala mayor para el Pokémon del jugador
        self.enemy_pokemon_scale_factor = 0.4  # Escala menor para el Pokémon enemigo

    def handle_events(self, event):
        """Maneja los eventos de la pantalla de combate."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Completa el texto inmediatamente si no ha sido mostrado por completo
            if not self.text_display_manager.is_dialogue_complete():
                self.text_display_manager.complete_text()
        return self

    def update(self):
        """Actualiza el estado de la pantalla de combate."""
        # Mover el Pokémon enemigo hacia su posición final
        if self.enemy_pokemon_current_pos[0] < self.enemy_pokemon_end_pos[0]:
            self.enemy_pokemon_current_pos[0] += self.pokemon_speed
            if self.enemy_pokemon_current_pos[0] > self.enemy_pokemon_end_pos[0]:
                self.enemy_pokemon_current_pos[0] = self.enemy_pokemon_end_pos[0]
                self.text_display_manager.set_text(self.encounter_text)

        # Actualizar el sistema de diálogo (para mostrar progresivamente el texto)
        self.text_display_manager.update()

    def draw(self, screen):
        """Dibuja la pantalla de combate."""
        screen_width = pygame.display.get_surface().get_width()
        screen.blit(self.background_image, (0, 0))

        self.draw_pokemon(screen, self.player_current_pokemon, self.player_pokemon_pos,
                          self.player_pokemon_scale_factor)  # Dibuja al pokemon del jugador
        ui.draw_combat_background(screen)
        self.draw_pokemon(screen, self.enemy_pokemon, self.enemy_pokemon_current_pos, self.enemy_pokemon_scale_factor)

        # Dibuja las cajas de estado (nombre, nivel, vida, etc.)
        box_width = 250
        ui.draw_combat_pokemon_status_box(screen, self.player_current_pokemon,
                                          (screen_width - box_width-1, 300), is_player_pokemon=True)
        ui.draw_combat_pokemon_status_box(screen, self.enemy_pokemon, (2, 50), is_player_pokemon=False)

        # Dibujar el recuadro para el texto
        ui.draw_dialog_box(screen)

        # Mostrar el texto de diálogo
        self.text_display_manager.draw(screen)

    @staticmethod
    def draw_pokemon(screen, pokemon, position, scale_factor):
        """Dibuja un Pokémon en la pantalla en la posición dada con el tamaño escalado."""
        if pokemon.image:
            scaled_image = pygame.transform.scale(pokemon.image, (
                int(pokemon.image.get_width() * scale_factor),
                int(pokemon.image.get_height() * scale_factor)
            ))
            screen.blit(scaled_image, position)

    @staticmethod
    def resize_image_to_width(image, new_width):
        """Redimensiona la imagen para que ajuste al nuevo ancho manteniendo las proporciones."""
        original_width, original_height = image.get_size()
        new_height = int((new_width / original_width) * original_height)
        resized_image = pygame.transform.scale(image, (new_width, new_height))
        return resized_image
