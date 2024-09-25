import pygame
import game.utils as utils
import game.ui as ui
from game.dialogue_manager import DialogueManager, TextDisplayManager
from game.save_load_manager import SaveLoadManager


class SaveGameScreen:
    def __init__(self, player):
        self.player = player

        # Cargar imagen de fondo
        self.background = utils.load_image("../assets/img/main_menu/fondo.png")
        self.background = pygame.transform.scale(self.background, (
            pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))

        # Gestión de diálogos
        self.dialogue_manager = DialogueManager("../game/data/dialogues.json")
        self.dialogue_manager.set_context('save_game')
        self.dialog_stage = 'save_prompt'
        self.current_line_index = 0
        self.text_display_manager = TextDisplayManager(pygame.font.Font(utils.load_font(), 35))

        # Estado inicial
        self.show_confirmation = False
        self.selected_confirmation_option = "no"
        self.saving_timer = None

        self.set_dialog_text()

    def handle_events(self, event):
        """Maneja los eventos del teclado y ratón."""
        if event.type == pygame.KEYDOWN:
            if self.saving_timer is not None or not self.text_display_manager.is_dialogue_complete():
                return self
            if event.key == pygame.K_RETURN:
                return self.handle_return_key()
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                if self.show_confirmation:
                    self.selected_confirmation_option = utils.handle_confirmation_navigation(
                        self.selected_confirmation_option, event.key
                    )
        return self

    def handle_return_key(self):
        """Maneja el evento de presionar Enter."""
        if self.dialog_stage == 'save_prompt':
            if self.selected_confirmation_option == 'yes':
                self.dialog_stage = 'saving_game'
                self.current_line_index = 0
                self.saving_timer = pygame.time.get_ticks() + 7000
                self.set_dialog_text()
            elif self.selected_confirmation_option == 'no':
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)
        elif self.dialog_stage == 'saved_game':
            from game.screen.main_menu_screen import MainMenuScreen
            return MainMenuScreen(self.player)
        return self

    def set_dialog_text(self):
        """Configura el texto del diálogo inicial basado en el índice actual."""
        text = self.dialogue_manager.get_dialogue(self.dialog_stage)[self.current_line_index]
        self.text_display_manager.set_text(text)

    def update(self):
        """Actualiza el texto del diálogo, carácter por carácter."""
        if self.dialog_stage == 'save_prompt' and self.text_display_manager.is_dialogue_complete():
            self.show_confirmation = True

        if self.saving_timer is not None:
            if pygame.time.get_ticks() > self.saving_timer:
                self.saving_timer = None
                self.dialog_stage = 'saved_game'
                self.current_line_index = 0
                self.set_dialog_text()

        self.text_display_manager.update()

    def draw(self, screen):
        """Dibuja el fondo, cuadro de guardado, cuadro diálogo y opciones de confirmación."""
        screen.blit(self.background, (0, 0))

        ui.draw_save_game_box(screen, self.player)

        ui.draw_dialog_box(screen)
        self.text_display_manager.draw(screen)

        if self.dialog_stage == 'save_prompt' and self.show_confirmation:
            confirmation_box_position = (screen.get_width() - 145, 449 - 140)
            utils.draw_confirmation_box(
                screen,
                self.selected_confirmation_option,
                position=confirmation_box_position,
                box_width=140,
                box_height=140
            )
