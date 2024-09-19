import json
import pygame
import ui


def replace_placeholders(text, placeholders):
    """
    Reemplaza los placeholders en un texto con los valores proporcionados.

    :param text: El texto con los placeholders, por ejemplo "Hola {nombre}"
    :param placeholders: Un diccionario con los valores a sustituir,
                         por ejemplo {"nombre": "Ash"}
    :return: El texto con los placeholders reemplazados.
    """
    for key, value in placeholders.items():
        text = text.replace(f"{{{key}}}", value)
    return text


class DialogueManager:
    def __init__(self, json_path):
        self.dialogues = self.load_dialogues(json_path)
        self.current_context = None
        self.current_dialogue = None

    @staticmethod
    def load_dialogues(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def set_context(self, context):
        """Configura el contexto del diálogo actual."""
        if context in self.dialogues:
            self.current_context = context
            self.current_dialogue = self.dialogues[context]
        else:
            raise ValueError(f"Contexto de diálogo '{context}' no encontrado.")

    def get_dialogue(self, key):
        """Obtiene el diálogo según la clave. Devuelve una lista de cadenas de texto."""
        if self.current_context and key in self.current_dialogue:
            return self.current_dialogue[key]
        else:
            raise ValueError(f"Diálogo con clave '{key}' no encontrado en el contexto '{self.current_context}'.")

    def get_dialogue_with_placeholders(self, key, placeholders):
        """Obtiene el diálogo con los placeholders reemplazados."""
        return [replace_placeholders(line, placeholders) for line in self.get_dialogue(key)]


class TextDisplayManager:
    def __init__(self, font, dialogue_speed=1):
        self.font = font
        self.dialogue_speed = dialogue_speed
        self.current_text = ""
        self.displayed_text = ""
        self.last_update_time = pygame.time.get_ticks()
        self.current_index = 0
        self.dialogue_complete = False

    def set_text(self, text):
        self.current_text = text
        self.displayed_text = ""
        self.current_index = 0
        self.dialogue_complete = False
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        """Actualiza el texto mostrado, carácter por carácter."""
        if not self.dialogue_complete:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time > self.dialogue_speed:
                self.last_update_time = current_time
                self.current_index += 1
                self.displayed_text = self.current_text[:self.current_index]

                # Verifica si todo el texto ya ha sido mostrado
                if self.current_index >= len(self.current_text):
                    self.dialogue_complete = True

    def draw(self, screen, box_position=(12, 449), box_width=780, box_height=150, padding=20, line_spacing=10,
             text_color=(0, 0, 0), vertical_offset=-15):
        """Dibuja el texto mostrado dentro del cuadro de diálogo, respetando el tamaño y alineación."""
        ui.draw_text_in_dialog_box(screen, self.displayed_text, self.font, box_position,
                                   box_width=box_width, box_height=box_height, text_color=text_color,
                                   padding=padding, line_spacing=line_spacing, vertical_offset=vertical_offset)

    def is_dialogue_complete(self):
        """Retorna True si el texto ya ha sido completamente mostrado."""
        return self.dialogue_complete

    def complete_text(self):
        """Marca el diálogo como completo e inmediatamente muestra todo el texto."""
        self.displayed_text = self.current_text
        self.dialogue_complete = True
