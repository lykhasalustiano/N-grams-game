import pygame
import sys
from game_logic import CrosswordGame
from pygame_ui import PygameUI, Button, show_instructions, play_game

def main_menu(ui):
    """Displays the main menu and handles user selection."""
    buttons = [
        Button(ui.width // 2 - 200, 300, 400, 60, "START NEW GAME", ui.font_medium, ui.colors),
        Button(ui.width // 2 - 200, 380, 400, 60, "HOW TO PLAY", ui.font_medium, ui.colors),
        Button(ui.width // 2 - 200, 460, 400, 60, "EXIT GAME", ui.font_medium, ui.colors)
    ]
    selected_button = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 3
                elif event.key == pygame.K_RETURN:
                    return str(selected_button + 1)
                elif event.key >= pygame.K_1 and event.key <= pygame.K_3:
                    return str(event.key - pygame.K_0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.is_clicked(mouse_pos):
                        return str(i + 1)

        ui.screen.fill(ui.colors.WHITE)
        pygame.draw.rect(ui.screen, ui.colors.BLACK, (0, 0, ui.width, ui.height), 5)

        title = ui.font_title.render("CROSSWORD CHALLENGE", True, ui.colors.BLACK)
        title_rect = title.get_rect(center=(ui.width // 2, 150))
        ui.screen.blit(title, title_rect)

        subtitle = ui.font_medium.render("Complete the sentence, find the word!", True, ui.colors.DARK_GRAY)
        subtitle_rect = subtitle.get_rect(center=(ui.width // 2, 200))
        ui.screen.blit(subtitle, subtitle_rect)

        for i, button in enumerate(buttons):
            button.set_hover(button.is_clicked(mouse_pos))
            button.set_selected(i == selected_button)
            button.draw(ui.screen)

        instruction1 = ui.font_small.render("Use arrow keys and ENTER, or click with mouse", True, ui.colors.DARK_GRAY)
        instruction2 = ui.font_small.render("Or press 1, 2, or 3 for quick selection", True, ui.colors.DARK_GRAY)
        ui.screen.blit(instruction1, (ui.width // 2 - instruction1.get_width() // 2, 600))
        ui.screen.blit(instruction2, (ui.width // 2 - instruction2.get_width() // 2, 630))

        pygame.display.flip()
        ui.clock.tick(60)

def main():
    """Entry point of the program."""
    ui = PygameUI()
    while True:
        choice = main_menu(ui)
        if choice == "1":
            play_game(ui)
        elif choice == "2":
            show_instructions(ui)
        elif choice == "3":
            pygame.quit()
            return

if __name__ == "__main__":
    main()