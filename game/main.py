import sys

import pygame

from game.player import Player
from game.screen.main_menu_screen import MainMenuScreen
from game.screen.title_screen import TitleScreen
import game.pokemon as pok

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # Medidas de la pantalla


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    player = Player("RAUL")
    player.get_starter("cranidos")
    player.pokemons[0].experience = int(player.pokemons[0].experience_to_next_level / 2)
    pokemon_data_list = pok.load_pokemon_data()
    for i in range(100):
        new_pokemon = pok.create_random_pokemon(pokemon_data_list)
        player.add_pokemon(new_pokemon)
    current_screen = MainMenuScreen(player)  # Pantalla inicial

    #current_screen = TitleScreen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Manejar eventos de la pantalla actual
            new_screen = current_screen.handle_events(event)
            if new_screen is None:
                running = False
            elif new_screen is not current_screen:
                current_screen = new_screen

        if running:
            current_screen.update()
            screen.fill((0, 0, 0))  # Limpiar pantalla
            current_screen.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
