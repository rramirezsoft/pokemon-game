import sys
import pygame
from game import utils, ui
from game.dialogue_manager import DialogueManager, TextDisplayManager
from game.screen.base_screen import BaseScreen
from game.screen.main_menu_screen import MainMenuScreen


class LoadGameScreen(BaseScreen):
    def __init__(self, player):
        super().__init__(player)

        self.background_image = utils.load_image("../assets/img/main_menu/load_menu.png", (800, 600))

        self.selected_box = 0
        self.boxes = [
            pygame.Rect(150, 40, 400, 300),  # Load Game
            pygame.Rect(150, 345, 400, 55),  # New Game
            pygame.Rect(150, 405, 400, 55),  # Options
            pygame.Rect(150, 465, 400, 55)  # Quit Game
        ]

        self.border_box_color = (218, 165, 32)
        self.selected_box_color = (255, 223, 0)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.sound_manager.play_sound_effect("click_button")
                if self.selected_box == 0:
                    return MainMenuScreen(self.player)
                elif self.selected_box == 1:
                    return DeleteGameScreen(self.player)
                elif self.selected_box == 2:
                    print("Options selected")
                elif self.selected_box == 3:
                    pygame.quit()
                    sys.exit()

            elif event.key == pygame.K_DOWN:
                # Mover la selección hacia abajo
                self.selected_box = (self.selected_box + 1) % 4
                self.sound_manager.play_sound_effect("click_button")
            elif event.key == pygame.K_UP:
                # Mover la selección hacia arriba
                self.selected_box = (self.selected_box - 1) % 4
                self.sound_manager.play_sound_effect("click_button")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verifica en qué caja se hizo clic
            for i in range(4):
                if self.boxes[i].collidepoint(mouse_x, mouse_y):
                    if self.selected_box == i:
                        self.sound_manager.play_sound_effect("click_button")
                        if i == 0:
                            return MainMenuScreen(self.player)
                        elif i == 1:
                            return DeleteGameScreen(self.player)
                        elif i == 2:
                            print("Options selected")
                        elif i == 3:
                            pygame.quit()
                            sys.exit()
                    else:
                        self.selected_box = i
                        self.sound_manager.play_sound_effect("click_button")

        return self

    def update(self):
        pass

    def draw(self, screen):

        screen_width, screen_height = screen.get_size()
        screen.blit(self.background_image, (0, 0))

        for i, box in enumerate(self.boxes):
            if i == self.selected_box:
                border_color = self.selected_box_color
            else:
                border_color = self.border_box_color

            if i == 0:
                ui.draw_save_load_game_box(screen, title="LOAD GAME", player=self.player,
                                           box_position=(screen_width // 4, 40),
                                           outer_border_color=border_color)
            elif i == 1:
                ui.draw_save_load_game_box(screen, text="NEW GAME", box_position=(screen_width // 4, 345),
                                           box_height=55, outer_border_color=border_color)
            elif i == 2:
                ui.draw_save_load_game_box(screen, text="OPTIONS", box_position=(screen_width // 4, 405),
                                           box_height=55, outer_border_color=border_color)
            elif i == 3:
                ui.draw_save_load_game_box(screen, text="QUIT GAME", box_position=(screen_width // 4, 465),
                                           box_height=55, outer_border_color=border_color)

        pygame.display.flip()


class DeleteGameScreen(BaseScreen):
    def __init__(self, player):
        super().__init__(player)

        self.background_color = (94, 102, 242)

        # Gestión de diálogos
        self.dialogue_manager = DialogueManager("../game/data/dialogues.json")
        self.dialogue_manager.set_context('delete_game')
        self.dialog_stage = 'delete_prompt'
        self.current_line_index = 0
        self.text_display_manager = TextDisplayManager(pygame.font.Font(utils.load_font(), 35), dialogue_speed=50)

        # Estado inicial
        self.show_confirmation = False
        self.selected_confirmation_option = "no"
        self.timer = None

        self.set_dialog_text()

    def handle_events(self, event):
        """Maneja los eventos del teclado y ratón."""
        return utils.handle_load_save_events(self, event=event)

    def handle_return_key(self):

        if self.dialog_stage == 'delete_prompt':
            if self.selected_confirmation_option == 'yes':
                self.show_confirmation = False
                self.dialog_stage = 'confirmation'
                self.current_line_index = 0
                self.selected_confirmation_option = 'no'
                self.set_dialog_text()
            else:
                return LoadGameScreen(self.player)
        elif self.dialog_stage == 'confirmation':
            if self.selected_confirmation_option == 'yes':
                self.dialog_stage = 'deleting_data'
                self.timer = pygame.time.get_ticks() + 7000
                self.set_dialog_text()
                self.delete_player_data()
            else:
                return LoadGameScreen(self.player)
        elif self.dialog_stage == 'deleted_data':
            from oak_intro_screen import OakIntroScreen
            return OakIntroScreen()
        return self

    def delete_player_data(self):
        """Elimina los datos del jugador de la base de datos."""
        player_id = self.player.player_id
        try:
            result = self.db_manager.collection.delete_one({"player_id": player_id})
            if result.deleted_count > 0:
                print(f"Eliminados datos del jugador {player_id}")
            else:
                print(f"No se encontraron datos del jugador {player_id}")
        except Exception as e:
            print(f"Error al eliminar datos del jugador {player_id}: {e}")

    def update(self):
        if ((self.dialog_stage == 'delete_prompt' or self.dialog_stage == 'confirmation')
                and self.text_display_manager.is_dialogue_complete()):
            self.show_confirmation = True

        if self.timer is not None:
            if pygame.time.get_ticks() > self.timer:
                self.timer = None
                self.dialog_stage = 'deleted_data'
                self.current_line_index = 0
                self.set_dialog_text()
        self.text_display_manager.update()

    def set_dialog_text(self):
        """Configura el texto del diálogo inicial basado en el índice actual."""
        text = self.dialogue_manager.get_dialogue(self.dialog_stage)[self.current_line_index]
        self.text_display_manager.set_text(text)

    def draw(self, screen):
        screen.fill(self.background_color)
        ui.draw_dialog_box(screen)
        self.text_display_manager.draw(screen)

        if (self.dialog_stage == 'delete_prompt' or self.dialog_stage == 'confirmation') and self.show_confirmation:
            confirmation_box_position = (screen.get_width() - 145, 449 - 140)
            utils.draw_confirmation_box(
                screen,
                self.selected_confirmation_option,
                position=confirmation_box_position,
                box_width=140,
                box_height=140
            )

        pygame.display.flip()
