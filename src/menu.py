import sys

import pygame

from Othello.src import settings

selected_option = None


def display_menu():
    title = settings.TITLE_FONT.render("Othello", True, settings.BLACK)
    window = (pygame
              .display
              .set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)))

    window.fill(settings.GREEN)
    window.blit(
        title,
        title.get_rect(center=(settings.WINDOW_WIDTH // 2, 50))
    )

    for i, option in enumerate(settings.OPTIONS):
        button = pygame.Rect(
            settings.WINDOW_WIDTH // 4,
            150 + i * 80,
            settings.WINDOW_WIDTH // 2,
            60
        )

        if selected_option == i:
            pygame.draw.rect(window, settings.LIGHT_BLUE, button)
        else:
            pygame.draw.rect(window, settings.WHITE, button)

        text = settings.FONT.render(
            option,
            True,
            settings.BLACK)
        window.blit(text, text.get_rect(center=button.center))


def menu():
    global selected_option
    playing = False
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                for selected_option, option in enumerate(settings.OPTIONS):

                    button = pygame.Rect(
                        settings.WINDOW_WIDTH // 4,
                        150 + selected_option * 80,
                        settings.WINDOW_WIDTH // 2, 60
                    )

                    if button.collidepoint(x, y):
                        if selected_option == 0:
                            print("Lancement du jeu Joueur vs. Joueur")
                            return "PVP"

                        elif selected_option == 1:
                            print("Lancement du jeu Joueur vs. IA")
                            return "PVIA"

                        elif selected_option == 2:
                            print("Lancement du jeu IA vs. IA")
                            return "IAVIA"

                        elif selected_option == 3:
                            pygame.quit()
                            sys.exit()

        if not playing:
            display_menu()

        pygame.display.flip()
        clock.tick(10)
