import random

import pygame


def is_music_playing():
    """Verifica si hay música en curso."""
    return pygame.mixer.music.get_busy()


class SoundManager:
    def __init__(self):
        pygame.mixer.init()  # Inicializar el mezclador de sonidos

        # Diccionarios para almacenar música y efectos de sonido
        self.music_tracks = {
            "opening": "../assets/sound/opening.mp3",
            "oak": "../assets/sound/oak.mp3",
            "battle": "../assets/sound/battle.mp3",
            "jubilife_city": "../assets/sound/jubilife_city.mp3",
            "lake": "../assets/sound/lake.mp3",
            "sandgem_town": "../assets/sound/sandgem_town.mp3",
            "twinleaf_town": "../assets/sound/twinleaf_town.mp3",
            "vitory": "../assets/sound/vitory.mp3"
        }
        self.sound_effects = {

        }

        # Inicialización de lista de música para el menú
        self.menu_music_tracks = [
            "jubilife_city",
            "lake",
            "sandgem_town",
            "twinleaf_town"
        ]

        # Volúmenes por defecto
        self.set_music_volume(0.5)
        self.set_sfx_volume(0.7)

        # Configurar evento que se disparará cuando la música termine
        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    # ----------------------------------
    # Métodos para la música
    # ----------------------------------

    def play_random_menu_music(self):
        """Reproduce una pista aleatoria del menú principal si no hay música en curso."""
        if not is_music_playing():
            random_track = random.choice(self.menu_music_tracks)
            self.play_music(random_track)

    def play_music(self, track_name, loop=0):
        """Reproduce una pista de música."""
        if track_name in self.music_tracks:
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.play(loop)

    @staticmethod
    def stop_music():
        """Detiene la música actual."""
        pygame.mixer.music.stop()

    @staticmethod
    def set_music_volume(volume):
        """Ajusta el volumen de la música. Valor entre 0.0 y 1.0."""
        pygame.mixer.music.set_volume(volume)

    @staticmethod
    def fadeout_music(time_ms):
        """Hace un fadeout de la música actual en el tiempo especificado en milisegundos."""
        pygame.mixer.music.fadeout(time_ms)

    # ----------------------------------
    # Métodos para efectos de sonido
    # ----------------------------------
    def play_sound_effect(self, effect_name):
        """Reproduce un efecto de sonido específico."""
        if effect_name in self.sound_effects:
            self.sound_effects[effect_name].play()

    def stop_sound_effect(self, effect_name):
        """Detiene un efecto de sonido en reproducción."""
        if effect_name in self.sound_effects:
            self.sound_effects[effect_name].stop()

    def set_sfx_volume(self, volume):
        """Ajusta el volumen global de los efectos de sonido. Valor entre 0.0 y 1.0."""
        for sound in self.sound_effects.values():
            sound.set_volume(volume)
