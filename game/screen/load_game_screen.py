import pygame
from game import utils, ui
from game.screen.main_menu_screen import MainMenuScreen
from game.screen.delete_game_screen import DeleteGameScreen


class LoadGameScreen:
    def __init__(self, player):
        self.player = player
        self.background_image = utils.load_image("../assets/img/main_menu/load_menu.png", (800, 600))

        self.selected_box = 0
        self.boxes = [
            pygame.Rect(150, 40, 400, 300),  # Load Game
            pygame.Rect(150, 345, 400, 55),  # New Game
            pygame.Rect(150, 405, 400, 55),  # Options
            pygame.Rect(150, 465, 400, 55)  # Quit Game
        ]

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.selected_box == 0:
                    return MainMenuScreen(self.player)
                elif self.selected_box == 1:
                    return DeleteGameScreen(self.player)
                elif self.selected_box == 2:
                    print("Options selected")
                elif self.selected_box == 3:
                    print("Quit Game selected")

            elif event.key == pygame.K_DOWN:
                # Mover la selección hacia abajo
                self.selected_box = (self.selected_box + 1) % 4
            elif event.key == pygame.K_UP:
                # Mover la selección hacia arriba
                self.selected_box = (self.selected_box - 1) % 4

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verifica en qué caja se hizo clic
            for i in range(4):
                if self.boxes[i].collidepoint(mouse_x, mouse_y):
                    if i == 0:
                        return MainMenuScreen(self.player)
                    elif i == 1:
                        return DeleteGameScreen(self.player)
                    elif i == 2:
                        print("Options selected")
                    elif i == 3:
                        print("Quit Game selected")
        return self

    def update(self):
        pass

    def draw(self, screen):

        screen_width, screen_height = screen.get_size()
        screen.blit(self.background_image, (0, 0))

        ui.draw_save_load_game_box(screen, title="LOAD GAME", player=self.player, box_position=(screen_width // 4, 40))
        ui.draw_save_load_game_box(screen, text="NEW GAME", box_position=(screen_width // 4, 345), box_height=55)
        ui.draw_save_load_game_box(screen, text="OPTIONS", box_position=(screen_width // 4, 405), box_height=55)
        ui.draw_save_load_game_box(screen, text="QUIT GAME", box_position=(screen_width // 4, 465), box_height=55)

        pygame.display.flip()
