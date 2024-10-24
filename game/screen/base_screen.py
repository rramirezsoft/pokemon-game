from game.database_manager import DataBaseManager, MONGO_URI
from game.sounds import SoundManager


class BaseScreen:
    def __init__(self, player):
        self.player = player
        self.sound_manager = SoundManager()
        self.db_manager = DataBaseManager(MONGO_URI)

    def handle_events(self, event):
        """Método que las pantallas específicas pueden sobrescribir"""
        pass

    def update(self):
        """Método que las pantallas específicas pueden sobrescribir"""
        pass

    def draw(self, screen):
        """Método que las pantallas específicas pueden sobrescribir"""
        pass
