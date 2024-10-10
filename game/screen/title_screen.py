import pygame

from game.screen.load_game_screen import LoadGameScreen
from game.utils import load_image, load_font, render_text
from game.screen.oak_intro_screen import OakIntroScreen
from game.sounds import SoundManager


class TitleScreen:
    def __init__(self):
        self.background_image = load_image("../assets/img/title/fondo.png", (800, 600))
        self.logo_image = load_image("../assets/img/title/logo_pokemon.png", (600, 250))
        self.pikachu_image = load_image("../assets/pokemon_images/pikachu.png", (350, 350))
        self.font_path = load_font()
        self.developer_text = render_text(self.font_path, 25, "Developed by RRamirezSoft \u00A9", (0, 0, 0))
        self.press_enter_text = render_text(self.font_path, 55, "Press Enter", (255, 0, 0))
        self.blink = True
        self.blink_time = 0
        self.blink_interval = 500

        # Música
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("opening")

    def handle_events(self, event):
        """Maneja los eventos del teclado."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.sound_manager.stop_music()
            return OakIntroScreen()  # Cambia a la pantalla para elegir nombre
        return self

    def update(self):
        """Actualiza la pantalla, incluyendo el parpadeo del texto."""
        current_time = pygame.time.get_ticks()
        if current_time - self.blink_time >= self.blink_interval:
            self.blink = not self.blink
            self.blink_time = current_time

    def draw(self, screen):
        """Dibuja la pantalla de bienvenida."""
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.logo_image, self.logo_image.get_rect(center=(400, 100)))
        screen.blit(self.pikachu_image, self.pikachu_image.get_rect(center=(400, 350)))
        if self.blink:
            screen.blit(self.press_enter_text, self.press_enter_text.get_rect(center=(400, 520)))
        screen.blit(self.developer_text, self.developer_text.get_rect(bottomleft=(10, 590)))
