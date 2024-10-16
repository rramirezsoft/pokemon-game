import pygame
from game import utils, ui
from game.database_manager import DataBaseManager, MONGO_URI
from game.dialogue_manager import DialogueManager, TextDisplayManager
from game.screen.oak_intro_screen import OakIntroScreen


class DeleteGameScreen:
    def __init__(self, player):
        self.player = player
        self.background_color = (94, 102, 242)

        # Inicializamos la base de datos
        self.db_manager = DataBaseManager(MONGO_URI)

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
        from game.screen.load_game_screen import LoadGameScreen

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
