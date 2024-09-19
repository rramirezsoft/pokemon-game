import pygame
import game.utils as utils
from game.screen.combat_screen import CombatScreen
from game.sounds import SoundManager


class BattleTransitionScreen:
    def __init__(self, player, enemy_pokemon):
        self.player = player
        self.enemy_pokemon = enemy_pokemon

        self.font = pygame.font.Font(utils.load_font(), 35)

        # Cargar imagen de la Pokébola
        self.pokeball_image = utils.load_image("../assets/img/icons/pokeball.png")

        # Configurar el tamaño inicial y final de la Pokébola
        self.initial_size = 50
        self.final_size = max(pygame.display.get_surface().get_width(),
                              pygame.display.get_surface().get_height()) * 1.8

        self.transition_complete = False
        self.rotation_angle = 0
        self.size = self.initial_size

        # Música
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("battle", loop=-1)

    def update(self):
        """Actualizar el estado de la animación"""
        if not self.transition_complete:
            # Incrementar el tamaño de la Pokébola
            size_increment = 10  # Cantidad de incremento por actualización
            if self.size < self.final_size:
                self.size += size_increment
                if self.size >= self.final_size:
                    self.size = self.final_size
                    self.transition_complete = True
            # Actualizar el ángulo de rotación solo mientras la animación está en curso
            self.rotation_angle += 3  # Velocidad de rotación (grados por frame)
            if self.rotation_angle >= 360:
                self.rotation_angle -= 360
        return self.size

    def draw(self, screen):
        """Dibuja la animación de transición"""
        size = self.update()
        pokeball_scaled = pygame.transform.scale(self.pokeball_image, (size, size))

        if not self.transition_complete:
            # Rotar la imagen de la Pokébola solo mientras la animación está en curso
            pokeball_rotated = pygame.transform.rotate(pokeball_scaled, self.rotation_angle)
        else:
            return CombatScreen(self.player, self.enemy_pokemon)

        # Calcular la posición para centrar la Pokébola
        x = (pygame.display.get_surface().get_width() - size) // 2
        y = (pygame.display.get_surface().get_height() - size) // 2

        # Ajustar la posición después de la rotación
        rotated_rect = pokeball_rotated.get_rect(center=(x + size // 2, y + size // 2))

        screen.blit(pokeball_rotated, rotated_rect.topleft)
        return self

    def handle_events(self, event):
        """Maneja los eventos mientras se muestra la transición"""
        if self.transition_complete:
            return CombatScreen(self.player, self.enemy_pokemon)
        return self
