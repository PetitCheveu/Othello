import sys

import pygame

from src import settings, board

selected_option = None
cursor_value = settings.MINIMAX_DEPTH


def display_menu(title=settings.CAPTION, option_list=settings.OPTIONS):
    window = board.display_background_and_title(title)

    for i, option in enumerate(option_list):
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

    return window


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


def display_ai_parameters(title):
    window = display_menu(title, settings.AVAILABLE_AIS)

    # Display the cursor and its value
    cursor_rect = pygame.Rect(
        settings.WINDOW_WIDTH // 4,
        450,
        settings.WINDOW_WIDTH // 2,
        60
    )

    pygame.draw.rect(
        window,
        settings.WHITE,
        cursor_rect
    )

    pygame.draw.rect(
        window,
        settings.BLACK,
        ((cursor_value - settings.MINIMAX_DEPTH) / (settings.MAXIMAL_DEPTH - settings.MINIMAX_DEPTH) * (
                cursor_rect.width - 20) + cursor_rect.x + 10,
         cursor_rect.y + 10,
         10,
         40)
    )

    text = settings.FONT.render(
        f"Nombre : {cursor_value}",
        True,
        settings.BLACK
    )

    window.blit(
        text,
        text.get_rect(center=cursor_rect.center)
    )


def ai_parameters(title):
    global selected_option
    global cursor_value
    cursor_dragging = False
    playing = False
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    cursor_rect = pygame.Rect(
        settings.WINDOW_WIDTH // 4,
        450,
        settings.WINDOW_WIDTH // 2,
        60
    )

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                for selected_option, option in enumerate(settings.AVAILABLE_AIS):

                    button = pygame.Rect(
                        settings.WINDOW_WIDTH // 4,
                        150 + selected_option * 80,
                        settings.WINDOW_WIDTH // 2,
                        60
                    )

                    if button.collidepoint(x, y):
                        if selected_option == 0:
                            print("Lancement d'Alphabeta1 avec nombre =", cursor_value)
                            return "Alphabeta1", cursor_value

                        elif selected_option == 1:
                            print("Lancement d'Alphabeta2 avec nombre =", cursor_value)
                            return "Alphabeta2", cursor_value

                        elif selected_option == 2:
                            print("Lancement de Minmax avec nombre =", cursor_value)
                            return "Minmax", cursor_value

                        elif selected_option == 3:
                            pygame.quit()
                            sys.exit()

                if cursor_rect.collidepoint(x, y):
                    cursor_dragging = True

            elif event.type == pygame.MOUSEMOTION and cursor_dragging:
                x, _ = event.pos
                cursor_value = int(((max(cursor_rect.left + 10,
                                         min(cursor_rect.right - 10, x)) - cursor_rect.left - 10) / (
                                            cursor_rect.width - 20)) * (
                                           settings.MAXIMAL_DEPTH - settings.MINIMAX_DEPTH) + settings.MINIMAX_DEPTH)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor_dragging = False

        if not playing:
            display_ai_parameters(title)

        pygame.display.flip()
        clock.tick(10)
