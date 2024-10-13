import pygame
import game.utils as utils


class ChooseNameScreen:
    def __init__(self, oak_intro_screen):
        self.oak_intro_screen = oak_intro_screen
        self.background_color = (255, 232, 127)
        self.font = pygame.font.Font(utils.load_font(), 40)
        self.font_large = pygame.font.Font(utils.load_font(), 60)

        # Parámetros del nombre
        self.max_name_length = 10
        self.current_name = ""

        # Tamaño de la pantalla
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        # Botones del teclado
        self.buttons = []
        self.create_keyboard_buttons()

        # Colores y sombras para la UI
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)
        self.text_color = (0, 0, 0)
        self.box_color = (255, 255, 255)
        self.container_color = (230, 164, 62)
        self.button_container_color = (250, 186, 88)

    def create_keyboard_buttons(self):
        """Crea los botones del teclado con letras y símbolos."""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        button_width, button_height = 60, 60
        padding = 10

        # Botones de confirmación y borrar estilizados
        total_width_action_buttons = 300 + padding
        x_action_start = (self.screen_width - total_width_action_buttons) // 2

        self.buttons.append(('DEL', pygame.Rect(x_action_start, 160, 130, 60)))
        self.buttons.append(('OK', pygame.Rect(x_action_start + 130 + padding, 160, 130, 60)))

        # Centramos el teclado horizontalmente y ajustamos su posición vertical más cerca de los botones "DEL" y "OK"
        total_keyboard_width = (button_width + padding) * 7 - padding
        x_start = (self.screen_width - total_keyboard_width) // 2
        y_start = 250

        for i, letter in enumerate(letters):
            x = x_start + (i % 7) * (button_width + padding)  # Distribuir 7 letras por fila
            y = y_start + (i // 7) * (button_height + padding)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append((letter, rect))

    def handle_events(self, event):
        """Maneja los eventos del mouse y teclado."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for letter, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return self.handle_button_click(letter)
        return self

    def handle_button_click(self, letter):
        """Acciones cuando se presiona un botón."""
        if letter == 'DEL':
            self.current_name = self.current_name[:-1]
        elif letter == 'OK' and self.current_name:
            # Confirma el nombre y vuelve a OakIntroScreen
            self.oak_intro_screen.player_name = self.current_name
            self.oak_intro_screen.set_dialog_text()
            return self.oak_intro_screen  # Regresa a la pantalla de Oak
        elif len(self.current_name) < self.max_name_length:
            self.current_name += letter
        return self  # Devolver la pantalla actual después de la acción

    def draw(self, screen):
        """Dibuja la pantalla de selección de nombre."""
        screen.fill(self.background_color)

        # Contenedor alrededor de la caja de texto y los botones
        container_width = 640
        container_height = 520
        container_rect = pygame.Rect((self.screen_width - container_width) // 2, 30, container_width, container_height)
        pygame.draw.rect(screen, self.container_color, container_rect, border_radius=15)

        # Caja de texto con el nombre actual centrada, con guiones bajos para letras faltantes
        name_box_width = 600
        name_box_height = 80
        name_box_rect = pygame.Rect((self.screen_width - name_box_width) // 2, 50, name_box_width, name_box_height)
        pygame.draw.rect(screen, self.box_color, name_box_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), name_box_rect, 3, border_radius=10)

        # Contenedor alrededor de los botones
        button_container_width = 550
        button_container_height = 390
        button_container_rect = pygame.Rect((self.screen_width - button_container_width) // 2, 145,
                                            button_container_width, button_container_height)
        pygame.draw.rect(screen, self.button_container_color, button_container_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_container_rect, 3,
                         border_radius=10)

        char_spacing = 40  # Espacio entre los caracteres
        start_x = (self.screen_width - (char_spacing * self.max_name_length)) // 2

        for i in range(self.max_name_length):
            char = self.current_name[i] if i < len(self.current_name) else '_'
            char_surface = self.font_large.render(char, True, self.text_color)

            # Posiciona los caracteres (letras o guiones bajos) de forma centrada
            char_x = start_x + char_spacing * i
            char_y = name_box_rect.y + (name_box_height - char_surface.get_height()) // 2

            screen.blit(char_surface, (char_x, char_y))

        # Dibuja los botones de "DEL" y "OK" justo debajo del cuadro del nombre
        for letter, rect in self.buttons:
            color = self.button_color
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = self.button_hover_color
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=10)

            # Dibuja el texto sobre cada botón
            text_surf = self.font.render(letter, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                                    rect.y + (rect.height - text_surf.get_height()) // 2))

        pygame.display.flip()

    def update(self):
        """Actualiza el estado de la pantalla."""
        pass
