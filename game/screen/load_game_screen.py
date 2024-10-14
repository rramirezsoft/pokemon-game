import pygame
import game.ui as ui
import game.utils as utils
from game.screen.main_menu_screen import MainMenuScreen


class LoadGameScreen:
    def __init__(self, player):
        self.player = player
        self.background_image = utils.load_image("../assets/img/main_menu/load_menu.png", (800, 600))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return MainMenuScreen(self.player)
        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

        ui.draw_save_load_game_box(screen, self.player)

        pygame.display.flip()
