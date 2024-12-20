import pygame
from game import ui, utils
from game.screen.base_screen import BaseScreen
from game.screen.save_game_screen import SaveGameScreen
from game.screen.pokemon_menu_screen import PokemonMenuScreen
from game.screen.pokedex_screen import PokedexScreen
from game.screen.trainer_card_screen import TrainerCardScreen
import game.pokemon as pokemon


class MainMenuScreen(BaseScreen):
    def __init__(self, player):
        super().__init__(player)
        self.font = pygame.font.Font(utils.load_font(), 35)

        # Cargar imagen de fondo
        self.background = utils.load_image("../assets/img/main_menu/fondo.png")
        self.background = pygame.transform.scale(self.background, (
            pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))

        # Cargar imágenes para los botones
        self.button_images = {
            "fight": utils.load_image("../assets/img/main_menu/icons/luchar.png"),
            "pokemon": utils.load_image("../assets/img/main_menu/icons/pokeball.png"),
            "bag": utils.load_image("../assets/img/main_menu/icons/bolsa.png"),
            "shop": utils.load_image("../assets/img/main_menu/icons/tienda.png"),
            "pokedex": utils.load_image("../assets/img/main_menu/icons/pokedex.png"),
            "player": utils.load_image("../assets/img/main_menu/icons/tarjeta.png"),
            "options": utils.load_image("../assets/img/main_menu/icons/ajustes.png"),
            "save": utils.load_image("../assets/img/main_menu/icons/guardar.png"),
        }

        # Crear botones con posiciones ajustadas y dimensiones más pequeñas
        self.buttons = {
            "fight": ui.Button("Fight", (80, 80, 150, 100), self.font, self.button_images["fight"]),
            "pokemon": ui.Button("Pokémon", (280, 80, 150, 100), self.font, self.button_images["pokemon"]),
            "bag": ui.Button("Bag", (80, 200, 150, 100), self.font, self.button_images["bag"]),
            "shop": ui.Button("Shop", (280, 200, 150, 100), self.font, self.button_images["shop"]),
            "pokedex": ui.Button("Pokédex", (80, 320, 150, 100), self.font, self.button_images["pokedex"]),
            "player": ui.Button(self.player.name, (280, 320, 150, 100), self.font, self.button_images["player"]),
            "options": ui.Button("Settings", (80, 440, 150, 100), self.font, self.button_images["options"]),
            "save": ui.Button("Save", (280, 440, 150, 100), self.font, self.button_images["save"]),
        }

        # Música
        self.sound_manager.play_random_menu_music()

    def handle_events(self, event):
        """Maneja los eventos del menú principal."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button_name, button in self.buttons.items():
                if button.is_clicked(mouse_pos):
                    self.sound_manager.play_sound_effect("click_button")
                    return self.handle_button_click(button_name)
        elif event.type == self.sound_manager.MUSIC_END_EVENT:
            self.sound_manager.play_random_menu_music()
        return self

    def handle_button_click(self, button_name):
        """Acciones cuando se hace clic en un botón."""
        if button_name == "fight":
            if not self.player.has_alive_pokemon():
                print("No tienes pokemon vivos")
            else:
                pokemon_date_list = pokemon.load_pokemon_data()
                enemy_pokemon = pokemon.create_random_pokemon(pokemon_date_list)
                return ui.start_battle_transition(self.player, enemy_pokemon)
        elif button_name == "pokemon":
            return PokemonMenuScreen(self.player)
        elif button_name == "bag":
            print("Abrir bolsa")
        elif button_name == "pokedex":
            return PokedexScreen(self.player)
        elif button_name == "player":
            return TrainerCardScreen(self.player)
        elif button_name == "options":
            print("Abrir opciones")
        elif button_name == "save":
            return SaveGameScreen(self.player)
        return self

    def update(self):
        """Actualizar el estado hover de los botones"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update(mouse_pos)

    def draw(self, screen):
        """Dibuja el menú principal."""

        # Dibujar fondo
        screen.blit(self.background, (0, 0))

        # Dibujar los botones
        for button in self.buttons.values():
            button.draw(screen)

        pygame.display.flip()
