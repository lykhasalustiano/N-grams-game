import pygame
import sys
import math
from game_logic import CrosswordGame # Make sure to import CrosswordGame

class Colors:
    """A simple class to hold color constants for readability."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)
    RED = (220, 20, 20)
    GREEN = (20, 200, 20)
    BLUE = (20, 20, 200)

class Button:
    """Represents a clickable button with hover and selected states."""
    def __init__(self, x, y, width, height, text, font, colors):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.colors = colors
        self.is_hovered = False
        self.is_selected = False

    def draw(self, screen):
        # Button background
        if self.is_selected:
            pygame.draw.rect(screen, self.colors.DARK_GRAY, self.rect)
            pygame.draw.rect(screen, self.colors.WHITE, self.rect, 3)
        elif self.is_hovered:
            pygame.draw.rect(screen, self.colors.LIGHT_GRAY, self.rect)
            pygame.draw.rect(screen, self.colors.BLACK, self.rect, 2)
        else:
            pygame.draw.rect(screen, self.colors.WHITE, self.rect)
            pygame.draw.rect(screen, self.colors.BLACK, self.rect, 2)

        # Button text
        text_color = self.colors.WHITE if self.is_selected else self.colors.BLACK
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """Checks if a given mouse position is inside the button."""
        return self.rect.collidepoint(pos)

    def set_hover(self, is_hovered):
        self.is_hovered = is_hovered
    
    def set_selected(self, is_selected):
        self.is_selected = is_selected

class PygameUI:
    """Manages all Pygame UI elements and rendering logic."""
    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Crossword Sentence Challenge")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_title = pygame.font.Font(None, 64)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)

        self.colors = Colors()

    def show_difficulty_selection(self):
        """Show difficulty selection with buttons."""
        buttons = [
            Button(self.width // 2 - 200, 300, 400, 60, "EASY - 60 seconds", self.font_medium, self.colors),
            Button(self.width // 2 - 200, 380, 400, 60, "MEDIUM - 45 seconds", self.font_medium, self.colors),
            Button(self.width // 2 - 200, 460, 400, 60, "HARD - 30 seconds", self.font_medium, self.colors)
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
                        return ["easy", "medium", "hard"][selected_button]
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_3:
                        return ["easy", "medium", "hard"][event.key - pygame.K_1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if button.is_clicked(mouse_pos):
                            return ["easy", "medium", "hard"][i]

            self.screen.fill(self.colors.WHITE)
            pygame.draw.rect(self.screen, self.colors.BLACK, (0, 0, self.width, self.height), 5)

            title = self.font_title.render("SELECT DIFFICULTY", True, self.colors.BLACK)
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)

            for i, button in enumerate(buttons):
                button.set_hover(button.is_clicked(mouse_pos))
                button.set_selected(i == selected_button)
                button.draw(self.screen)

            instruction1 = self.font_small.render("Use arrow keys and ENTER, or click with mouse", True, self.colors.DARK_GRAY)
            instruction2 = self.font_small.render("Or press 1, 2, or 3 for quick selection", True, self.colors.DARK_GRAY)
            self.screen.blit(instruction1, (self.width // 2 - instruction1.get_width() // 2, 600))
            self.screen.blit(instruction2, (self.width // 2 - instruction2.get_width() // 2, 630))

            pygame.display.flip()
            self.clock.tick(60)

    def draw_crossword_grid(self, word_length, filled_letters="", correct_word="", show_solution=False):
        """Draw a detailed crossword grid."""
        cell_size = 50
        grid_width = word_length * cell_size
        start_x = (self.width - grid_width) // 2
        start_y = 350

        pygame.draw.rect(self.screen, self.colors.LIGHT_GRAY, (start_x - 10, start_y - 10, grid_width + 20, cell_size + 20))
        pygame.draw.rect(self.screen, self.colors.BLACK, (start_x - 10, start_y - 10, grid_width + 20, cell_size + 20), 3)

        for i in range(word_length):
            x, y = start_x + i * cell_size, start_y
            pygame.draw.rect(self.screen, self.colors.WHITE, (x, y, cell_size, cell_size))
            pygame.draw.rect(self.screen, self.colors.BLACK, (x, y, cell_size, cell_size), 2)
            number_surface = self.font_tiny.render(str(i + 1), True, self.colors.DARK_GRAY)
            self.screen.blit(number_surface, (x + 2, y + 2))

            if show_solution and i < len(correct_word):
                letter_surface = self.font_large.render(correct_word[i].upper(), True, self.colors.BLACK)
                letter_rect = letter_surface.get_rect(center=(x + cell_size // 2, y + cell_size // 2 + 5))
                self.screen.blit(letter_surface, letter_rect)
            elif i < len(filled_letters):
                letter_surface = self.font_large.render(filled_letters[i].upper(), True, self.colors.BLACK)
                letter_rect = letter_surface.get_rect(center=(x + cell_size // 2, y + cell_size // 2 + 5))
                self.screen.blit(letter_surface, letter_rect)

    def draw_game_info_panel(self, score, lives, game_round, time_remaining, time_multiplier, base_time):
        """Draw comprehensive game info panel."""
        panel_width, panel_height = 350, 200
        panel_x, panel_y = self.width - panel_width - 20, 20

        pygame.draw.rect(self.screen, self.colors.LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, self.colors.BLACK, (panel_x, panel_y, panel_width, panel_height), 3)

        title = self.font_medium.render("GAME STATUS", True, self.colors.BLACK)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))

        y_offset = 50
        info_items = [
            f"Round: {game_round}/10",
            f"Score: {score}",
            f"Lives: {lives}",
            f"Time: {int(time_remaining)}s"
        ]

        for item in info_items:
            text_color = self.colors.RED if "Lives:" in item and lives <= 1 else self.colors.BLACK
            if "Time:" in item and time_remaining < 10:
                text_color = self.colors.RED
            text = self.font_small.render(item, True, text_color)
            self.screen.blit(text, (panel_x + 20, panel_y + y_offset))
            y_offset += 25

        if time_multiplier > 1.0:
            speed_text = f"TIMER SPEED: {time_multiplier:.1f}x"
            speed_surface = self.font_small.render(speed_text, True, self.colors.RED)
            self.screen.blit(speed_surface, (panel_x + 20, panel_y + y_offset))
            y_offset += 25

        bar_width, bar_height = 300, 20
        bar_x, bar_y = panel_x + 25, panel_y + y_offset

        pygame.draw.rect(self.screen, self.colors.WHITE, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, self.colors.BLACK, (bar_x, bar_y, bar_width, bar_height), 2)

        timer_percentage = max(0, min(1, time_remaining / base_time))
        filled_width = int(bar_width * timer_percentage)
        
        if time_remaining < 10:
            fill_color = self.colors.RED
        elif time_remaining < 20:
            fill_color = (255, 165, 0)
        else:
            fill_color = self.colors.GREEN

        if filled_width > 0:
            pygame.draw.rect(self.screen, fill_color, (bar_x, bar_y, filled_width, bar_height))

    def show_question(self, question, score, lives, game_round, time_remaining, time_multiplier, base_time):
        """Show crossword question with proper UI."""
        button_width, button_height = 400, 50
        buttons = []
        for i, option in enumerate(question['options']):
            y_pos = 500 + i * 60
            button = Button(
                self.width // 2 - button_width // 2, y_pos, button_width, button_height,
                f"{i+1}. {option.upper()}", self.font_medium, self.colors
            )
            buttons.append(button)

        selected_option = 0
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: selected_option = (selected_option - 1) % 4
                    elif event.key == pygame.K_DOWN: selected_option = (selected_option + 1) % 4
                    elif event.key == pygame.K_RETURN: return selected_option
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_4: return event.key - pygame.K_1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if button.is_clicked(mouse_pos): return i
            if time_remaining <= 0: return -1

            self.screen.fill(self.colors.WHITE)
            pygame.draw.rect(self.screen, self.colors.BLACK, (0, 0, self.width, self.height), 5)
            self.draw_game_info_panel(score, lives, game_round, time_remaining, time_multiplier, base_time)

            title = self.font_large.render("COMPLETE THE SENTENCE", True, self.colors.BLACK)
            title_rect = title.get_rect(center=(self.width // 2, 50))
            self.screen.blit(title, title_rect)

            sentence_text = f'"{question["sentence"]} _____"'
            sentence_surface = self.font_medium.render(sentence_text, True, self.colors.BLACK)
            sentence_rect = sentence_surface.get_rect(center=(self.width // 2, 120))
            self.screen.blit(sentence_surface, sentence_rect)

            hint_text = f"Missing word has {question['length']} letters"
            hint_surface = self.font_small.render(hint_text, True, self.colors.DARK_GRAY)
            hint_rect = hint_surface.get_rect(center=(self.width // 2, 160))
            self.screen.blit(hint_surface, hint_rect)

            crossword_title = self.font_medium.render("CROSSWORD GRID", True, self.colors.BLACK)
            crossword_title_rect = crossword_title.get_rect(center=(self.width // 2, 250))
            self.screen.blit(crossword_title, crossword_title_rect)
            self.draw_crossword_grid(question['length'])

            choices_title = self.font_medium.render("CHOOSE YOUR ANSWER:", True, self.colors.BLACK)
            choices_rect = choices_title.get_rect(center=(self.width // 2, 450))
            self.screen.blit(choices_title, choices_rect)

            for i, button in enumerate(buttons):
                button.set_hover(button.is_clicked(mouse_pos))
                button.set_selected(i == selected_option)
                button.draw(self.screen)

            instruction = self.font_small.render("Use arrow keys + ENTER, number keys 1-4, or click", True, self.colors.DARK_GRAY)
            instruction_rect = instruction.get_rect(center=(self.width // 2, 750))
            self.screen.blit(instruction, instruction_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def show_feedback(self, message, is_correct, correct_word="", duration=3):
        """Show feedback with crossword solution."""
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration * 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: return

            self.screen.fill(self.colors.WHITE)
            pygame.draw.rect(self.screen, self.colors.BLACK, (0, 0, self.width, self.height), 5)
            color = self.colors.GREEN if is_correct else self.colors.RED
            result_text = "CORRECT!" if is_correct else "WRONG!"
            feedback_surface = self.font_title.render(result_text, True, color)
            feedback_rect = feedback_surface.get_rect(center=(self.width // 2, 200))
            self.screen.blit(feedback_surface, feedback_rect)

            if correct_word:
                solution_text = self.font_large.render("CORRECT ANSWER:", True, self.colors.BLACK)
                solution_rect = solution_text.get_rect(center=(self.width // 2, 300))
                self.screen.blit(solution_text, solution_rect)
                self.draw_crossword_grid(len(correct_word), correct_word=correct_word, show_solution=True)
                word_display = self.font_large.render(correct_word.upper(), True, self.colors.BLACK)
                word_rect = word_display.get_rect(center=(self.width // 2, 450))
                self.screen.blit(word_display, word_rect)

            if "!" in message:
                extra_msg = message.split("!")[1].strip()
                if extra_msg:
                    extra_surface = self.font_medium.render(extra_msg, True, self.colors.BLACK)
                    extra_rect = extra_surface.get_rect(center=(self.width // 2, 500))
                    self.screen.blit(extra_surface, extra_rect)
            
            skip_text = self.font_small.render("Press any key to continue...", True, self.colors.DARK_GRAY)
            skip_rect = skip_text.get_rect(center=(self.width // 2, 600))
            self.screen.blit(skip_text, skip_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def show_game_over(self, score, final_message):
        """Show game over screen with final stats."""
        button = Button(self.width // 2 - 200, 500, 400, 60, "RETURN TO MAIN MENU", self.font_medium, self.colors)
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and button.is_clicked(mouse_pos)):
                    return

            self.screen.fill(self.colors.WHITE)
            pygame.draw.rect(self.screen, self.colors.BLACK, (0, 0, self.width, self.height), 5)

            color = self.colors.GREEN if "CONGRATULATIONS" in final_message else self.colors.RED
            message_surface = self.font_title.render(final_message, True, color)
            message_rect = message_surface.get_rect(center=(self.width // 2, 200))
            self.screen.blit(message_surface, message_rect)

            score_text = f"FINAL SCORE: {score}/10"
            score_surface = self.font_large.render(score_text, True, self.colors.BLACK)
            score_rect = score_surface.get_rect(center=(self.width // 2, 300))
            self.screen.blit(score_surface, score_rect)

            if score >= 8: rating, rating_color = "EXCELLENT!", self.colors.GREEN
            elif score >= 6: rating, rating_color = "GOOD JOB!", self.colors.BLACK
            elif score >= 4: rating, rating_color = "NOT BAD!", self.colors.BLACK
            else: rating, rating_color = "KEEP TRYING!", self.colors.RED
            
            rating_surface = self.font_medium.render(rating, True, rating_color)
            rating_rect = rating_surface.get_rect(center=(self.width // 2, 350))
            self.screen.blit(rating_surface, rating_rect)

            button.set_hover(button.is_clicked(mouse_pos))
            button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

def show_instructions(ui):
    """
    Displays the game instructions screen with a two-panel layout.
    """
    back_button = Button(ui.width // 2 - 150, 650, 300, 50, "BACK TO MENU", ui.font_medium, ui.colors)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and back_button.is_clicked(mouse_pos)): return

        ui.screen.fill(ui.colors.WHITE)
        pygame.draw.rect(ui.screen, ui.colors.BLACK, (0, 0, ui.width, ui.height), 5)
        title = ui.font_title.render("HOW TO PLAY", True, ui.colors.BLACK)
        title_rect = title.get_rect(center=(ui.width // 2, 60))
        ui.screen.blit(title, title_rect)

        panel_width, panel_height, panel_y = 550, 450, 120
        left_panel_x, right_panel_x = 50, ui.width - panel_width - 50

        # --- Left Panel: Game Rules ---
        pygame.draw.rect(ui.screen, ui.colors.LIGHT_GRAY, (left_panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(ui.screen, ui.colors.BLACK, (left_panel_x, panel_y, panel_width, panel_height), 3)
        rules_title = ui.font_medium.render("GAME RULES", True, ui.colors.BLACK)
        ui.screen.blit(rules_title, (left_panel_x + 20, panel_y + 20))
        rules = [ "• Complete 10 sentence puzzles", "• Find the missing word in each sentence", "• Choose from 4 multiple choice options", "• You have 3 lives total", "", "TIMER SYSTEM:", "• Correct answer: +30 seconds", "• Wrong answer: Timer goes 2x faster", "• Timer resets to normal speed after correct answer", "", "DIFFICULTY LEVELS:", "• Easy: 60 seconds base time, simple words", "• Medium: 45 seconds base time", "• Hard: 30 seconds base time, complex words", "", "WIN CONDITION:", "Complete all 10 rounds to win!" ]
        y_pos = panel_y + 60
        for rule in rules:
            if not rule: y_pos += 15; continue
            color = ui.colors.BLACK if not rule.startswith("•") else ui.colors.DARK_GRAY
            rule_font = ui.font_small if not rule.startswith("•") else ui.font_tiny
            text = rule_font.render(rule, True, color)
            ui.screen.blit(text, (left_panel_x + 30, y_pos)); y_pos += 20

        # --- Right Panel: Controls ---
        pygame.draw.rect(ui.screen, ui.colors.LIGHT_GRAY, (right_panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(ui.screen, ui.colors.BLACK, (right_panel_x, panel_y, panel_width, panel_height), 3)
        controls_title = ui.font_medium.render("CONTROLS", True, ui.colors.BLACK)
        ui.screen.blit(controls_title, (right_panel_x + 20, panel_y + 20))
        controls = [ "KEYBOARD CONTROLS:", "• Arrow Keys (Up/Down): Navigate menu options", "• ENTER: Select an option", "• Number Keys (1-4): Quick selection of options", "", "MOUSE CONTROLS:", "• Click: Select a button or option" ]
        y_pos = panel_y + 60
        for control in controls:
            if not control: y_pos += 15; continue
            color = ui.colors.BLACK if not control.startswith("•") else ui.colors.DARK_GRAY
            control_font = ui.font_small if not control.startswith("•") else ui.font_tiny
            text = control_font.render(control, True, color)
            ui.screen.blit(text, (right_panel_x + 30, y_pos)); y_pos += 20
        
        back_button.set_hover(back_button.is_clicked(mouse_pos))
        back_button.draw(ui.screen)
        pygame.display.flip()
        ui.clock.tick(60)

def play_game(ui):
    """Main game loop for a new game session."""
    game = CrosswordGame()
    difficulty = ui.show_difficulty_selection()
    game.set_difficulty(difficulty)

    while not game.is_game_over():
        question = game.get_new_question()
        if not question: break

        while True:
            current_time = game.update_timer()
            if current_time <= 0:
                selected_option = -1
                break
            selected_option = ui.show_question(
                question, game.score, game.lives, game.round_number, current_time, game.time_multiplier, game.base_time
            )
            if selected_option is not None: break

        is_correct, message = game.check_answer(selected_option)
        ui.show_feedback(message, is_correct, correct_word=question['answer'] if not is_correct else None)

    final_message = game.get_final_message()
    ui.show_game_over(game.score, final_message)