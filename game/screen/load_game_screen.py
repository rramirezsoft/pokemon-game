import pygame
import game.ui as ui
from game.player import Player


class LoadGameScreen:
    def __init__(self):
        self.background_color = (154, 214, 255)
        self.player = Player("RAUL")

    def handle_events(self, event):
        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.background_color)
        ui.draw_save_game_box(screen, self.player)
