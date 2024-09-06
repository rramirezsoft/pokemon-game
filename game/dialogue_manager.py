import json


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
