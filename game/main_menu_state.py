import pygame
from utils import load_image, load_font, render_text


class MainMenuState:
    def __init__(self):
        self.background_image = load_image("../assets/img/fondo.png", (800, 600))
        self.font_path = load_font()
        self.menu_text = render_text(self.font_path, 30, "Main Menu", (255, 255, 255))

    def handle_events(self, event):
        """Maneja los eventos del teclado."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return None  # Salir del juego o regresar al título

        # Aquí puedes agregar más eventos específicos para el menú principal
        return self

    def update(self):
        """Actualiza el estado del menú principal."""
        pass

    def draw(self, screen):
        """Dibuja el menú principal."""
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.menu_text, self.menu_text.get_rect(center=(400, 300)))
