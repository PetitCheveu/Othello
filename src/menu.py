import sys

import pygame

from src import settings, board

selected_option = None
selected_ai = None
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
                        if selected_option == 3:
                            pygame.quit()
                            sys.exit()

                        else:
                            print(f"Lancement du jeu {settings.OPTIONS[selected_option]}")
                            return settings.OPTIONS[selected_option]

        if not playing:
            display_menu()

        pygame.display.flip()
        clock.tick(10)


def display_ai_parameters(title, selected_ai):
    window = board.display_background_and_title(title)
    offset = 0

    for i, option in enumerate(settings.AVAILABLE_AIS.keys()):
        if selected_ai is not None and i > selected_ai:
            offset = 40 * len(settings.AVAILABLE_AIS[list(settings.AVAILABLE_AIS.keys())[selected_ai]])

        button = pygame.Rect(
            settings.WINDOW_WIDTH // 4,
            150 + i * 80 + offset,
            settings.WINDOW_WIDTH // 2,
            60
        )

        if selected_option == i:
            pygame.draw.rect(window, settings.LIGHT_BLUE, button)
        else:
            pygame.draw.rect(window, settings.WHITE, button)

        sub_text = settings.FONT.render(
            option,
            True,
            settings.BLACK)
        window.blit(sub_text, sub_text.get_rect(center=button.center))

    if selected_ai is not None:
        ai_name = list(settings.AVAILABLE_AIS.keys())[selected_ai]
        eval_methods = settings.AVAILABLE_AIS[ai_name]

        for i, eval_method in enumerate(eval_methods):
            sub_button = pygame.Rect(
                settings.WINDOW_WIDTH // 3,
                180 + selected_ai * 80 + (i + 1) * 40,
                settings.WINDOW_WIDTH // 3,
                30
            )
            if sub_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window, settings.LIGHT_BLUE, sub_button)
            else:
                pygame.draw.rect(window, settings.WHITE, sub_button)

            sub_text = settings.FONT.render(
                eval_method,
                True,
                settings.BLACK)
            window.blit(sub_text, sub_text.get_rect(center=sub_button.center))

    # Display the cursor and its value
    cursor_rect = pygame.Rect(
        settings.WINDOW_WIDTH // 4,
        150 + len(settings.AVAILABLE_AIS.keys()) * 80 + (40 * len(settings.AVAILABLE_AIS[
                                                                      list(settings.AVAILABLE_AIS.keys())[
                                                                          selected_ai]]) if selected_ai is not None else 0),
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
                cursor_rect.width - 30) + cursor_rect.x + 10,
         cursor_rect.y + 10,
         10,
         40)
    )

    sub_text = settings.FONT.render(
        f"Profondeur : {cursor_value}",
        True,
        settings.BLACK
    )

    window.blit(
        sub_text,
        sub_text.get_rect(center=cursor_rect.center)
    )


def ai_parameters(title):
    global selected_option
    global cursor_value
    global selected_ai
    cursor_dragging = False
    playing = False
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():

            cursor_rect = pygame.Rect(
                settings.WINDOW_WIDTH // 4,
                150 + len(settings.AVAILABLE_AIS.keys()) * 80 + (40 * len(settings.AVAILABLE_AIS[
                                                                              list(
                                                                                  settings.AVAILABLE_AIS.keys())[
                                                                                  selected_ai]]) if selected_ai is not None else 0),
                settings.WINDOW_WIDTH // 2,
                60
            )

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                for selected_option, option in enumerate(settings.AVAILABLE_AIS):
                    offset = 0

                    if selected_ai is not None and selected_option > selected_ai:
                        offset = 40 * len(settings.AVAILABLE_AIS[list(settings.AVAILABLE_AIS.keys())[selected_ai]])

                    button = pygame.Rect(
                        settings.WINDOW_WIDTH // 4,
                        150 + selected_option * 80 + offset,
                        settings.WINDOW_WIDTH // 2,
                        60
                    )

                    if button.collidepoint(x, y):
                        if selected_ai == selected_option:
                            selected_ai = None
                        else:
                            selected_ai = selected_option
                        break

                if selected_ai is not None:
                    ai_name = list(settings.AVAILABLE_AIS.keys())[selected_ai]
                    eval_methods = settings.AVAILABLE_AIS[ai_name]

                    for i, eval_method in enumerate(eval_methods):
                        sub_button = pygame.Rect(
                            settings.WINDOW_WIDTH // 3,
                            180 + selected_ai * 80 + (i + 1) * 40,
                            settings.WINDOW_WIDTH // 3,
                            30
                        )
                        if sub_button.collidepoint(x, y):
                            print("Lancement de l'IA", ai_name,
                                  "avec la méthode d'évaluation", eval_method,
                                  "et la profondeur", cursor_value)
                            reset_interface()
                            return ai_name, eval_method, cursor_value, settings.MAX_TIMEOUT

                if cursor_rect.collidepoint(x, y):
                    cursor_dragging = True

            elif event.type == pygame.MOUSEMOTION and cursor_dragging:
                x, _ = event.pos
                cursor_value = round(int(((max(cursor_rect.left + 10,
                                               min(cursor_rect.right - 10, x)) - cursor_rect.left - 10) / (
                                                  cursor_rect.width - 20)) * (
                                                 settings.MAXIMAL_DEPTH - settings.MINIMAX_DEPTH) + settings.MINIMAX_DEPTH) / 2) * 2

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor_dragging = False

        if not playing:
            display_ai_parameters(title, selected_ai)

        pygame.display.flip()
        clock.tick(10)


def reset_interface():
    global selected_option
    global cursor_value
    global selected_ai
    selected_option = None
    cursor_value = settings.MINIMAX_DEPTH
    selected_ai = None
