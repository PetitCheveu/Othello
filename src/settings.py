import pygame

# Initialize Pygame
pygame.init()

# Window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CAPTION = "Othello"

# Colors
GREEN = (42, 81, 45)
WHITE = (255, 255, 255)
LIGHT_BLUE = (161, 212, 164)
BLACK = (0, 0, 0)

# Text settings
FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)

# Menu settings
OPTIONS = ["Joueur vs. Joueur", "Joueur vs. IA", "IA vs. IA", "Quitter"]
