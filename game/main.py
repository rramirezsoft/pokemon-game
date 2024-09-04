import pygame
import os
from utils import load_image, load_all_pokemon_images

# Inicializar Pygame y configurar la ventana
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pokémon Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar imágenes
background_image = load_image("../assets/img/fondo.png", (WINDOW_WIDTH, WINDOW_HEIGHT))
logo_image = load_image("../assets/img/logo_pokemon.png",(600, 250))

# Cargar imágenes de todos los Pokemon
images = load_all_pokemon_images(scale=(350, 350))

# Fuente para el texto
small_font = pygame.font.Font(None, 24)  # Puedes cambiar esto a una fuente personalizada
developer_text = small_font.render("Developed by RRamirezSoft \u00A9", True, WHITE)


# Dibujar pantalla de bienvenida
def draw_welcome_screen():
    screen.blit(background_image, (0, 0))  # Dibujar el fondo
    screen.blit(logo_image, logo_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5)))

    # Dibujar la imagen de Pikachu si está disponible en el directorio de Pokémon
    if 'pikachu' in images:
        screen.blit(images['pikachu'], images['pikachu'].get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)))

    screen.blit(developer_text, developer_text.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10)))
    pygame.display.flip()


# Bucle principal
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_welcome_screen()
        pygame.time.Clock().tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
