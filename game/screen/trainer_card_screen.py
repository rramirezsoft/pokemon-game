import pygame
from game import utils, ui
from game.screen.base_screen import BaseScreen
from game.ui import Footer


class TrainerCardScreen(BaseScreen):
    def __init__(self, player):
        super().__init__(player)

        self.background_color = (154, 252, 229)  # Color de fondo

        # Cargar la imagen de la ficha del entrenador
        self.trainer_card = utils.load_image("../assets/img/main_menu/ficha_entrenador.png")

        # Redimensionar la ficha del entrenador a un tamaño considerable (por ejemplo, el 70% del ancho de la pantalla)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        card_width = int(screen_width * 0.95)
        card_height = int(self.trainer_card.get_height() * (card_width / self.trainer_card.get_width()))
        self.trainer_card = pygame.transform.scale(self.trainer_card, (card_width, card_height))

        # Calcular la posición para centrar la ficha en la pantalla
        self.trainer_card_rect = self.trainer_card.get_rect(center=(screen_width // 2, screen_height // 2))

        # Crear el footer
        self.footer = Footer(buttons=[
            {"text": "Badges", "icon_path": "../assets/img/keyboard/x_blanco.png"}
        ],
            footer_color=(98, 161, 217))

    def handle_events(self, event):
        """
        Maneja los eventos del teclado de la pantalla.
        """
        if event.type == pygame.KEYDOWN:
            # Si se presiona ESC o BACKSPACE, vuelve al Main Menu
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                from game.screen.main_menu_screen import MainMenuScreen
                return MainMenuScreen(self.player)

            # Si se presiona la tecla X, ir a la pantalla de Badges
            elif event.key == pygame.K_x:
                return BadgesScreen(self.player)

        # Manejar eventos de clic en el footer
        footer_button = self.footer.handle_events(event)

        if footer_button == "Back":
            # Si se clicó el botón "Back", volver al Main Menu
            from game.screen.main_menu_screen import MainMenuScreen
            return MainMenuScreen(self.player)

        elif footer_button == "Badges":
            # Si se clicó el botón "Badges", ir a la pantalla de Badges
            return BadgesScreen(self.player)

        return self

    def update(self):
        pass

    def draw(self, screen):
        # Rellenar el fondo con el color en lugar de usar una imagen
        screen.fill(self.background_color)

        # Dibujar la ficha del entrenador en el centro de la pantalla
        screen.blit(self.trainer_card, self.trainer_card_rect.topleft)

        # Dibujar el footer
        self.footer.draw(screen)

        # Actualizar la pantalla
        pygame.display.flip()


class BadgesScreen(BaseScreen):
    def __init__(self, player):
        super().__init__(player)

        self.background_color = (154, 252, 229)  # Color de fondo

        # Crear el footer
        self.footer = Footer(footer_color=(98, 161, 217))

    def handle_events(self, event):
        """
        Maneja los eventos del teclado de la pantalla.
        """
        if event.type == pygame.KEYDOWN:
            # Si se presiona ESC o BACKSPACE, vuelve al Main Menu
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                return TrainerCardScreen(self.player)

        # Manejar eventos de clic en el footer
        if self.footer.handle_events(event):
            return TrainerCardScreen(self.player)

        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.background_color)

        self.footer.draw(screen)
        pygame.display.flip()
