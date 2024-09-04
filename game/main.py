import pygame
from title_state import TitleState

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # Medidas de la pantalla


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    current_state = TitleState()  # Estado inicial

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Manejar eventos del estado actual
            new_state = current_state.handle_events(event)
            if new_state is None:
                running = False
            elif new_state is not current_state:
                current_state = new_state

        current_state.update()
        screen.fill((0, 0, 0))  # Limpiar pantalla
        current_state.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
