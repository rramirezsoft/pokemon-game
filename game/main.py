import pygame
from game.screen.title_screen import TitleScreen


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # Medidas de la pantalla


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    current_screen = TitleScreen()  # Pantalla inicial

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

        current_screen.update()
        screen.fill((0, 0, 0))  # Limpiar pantalla
        current_screen.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
