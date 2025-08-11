import pygame
import sys
from colors import Colors

class PygameUI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Crossword Sentence Challenge")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.colors = Colors()
        
        # Load background image (optional)
        try:
            self.background = pygame.image.load("background.jpg")
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            self.background = None

    def show_intro(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))  # Dark blue background
            
            title = self.font_large.render("CROSSWORD SENTENCE CHALLENGE", True, self.colors.CYAN)
            subtitle = self.font_medium.render("Complete the sentence with the missing word", True, self.colors.YELLOW)
            instruction1 = self.font_small.render("You have 60 seconds for each word", True, self.colors.BLUE)
            instruction2 = self.font_small.render("3 wrong answers and the game is over", True, self.colors.RED)
            prompt = self.font_medium.render("Press any key to start...", True, self.colors.GREEN)
            
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            self.screen.blit(subtitle, (self.width//2 - subtitle.get_width()//2, 200))
            self.screen.blit(instruction1, (self.width//2 - instruction1.get_width()//2, 250))
            self.screen.blit(instruction2, (self.width//2 - instruction2.get_width()//2, 300))
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, 400))
            
            pygame.display.flip()
            self.clock.tick(30)

    def show_question(self, question, score, lives, time_remaining):
        self.screen.fill((0, 0, 50))  # Dark blue background
        
        # Score and timer display
        score_text = self.font_medium.render(f"Score: {score} | Lives: {lives}", True, self.colors.WHITE)
        time_text = self.font_medium.render(f"Time: {time_remaining:.1f}s", True, 
                                          self.colors.GREEN if time_remaining > 10 else self.colors.RED)
        
        # Question display
        instruction = self.font_small.render("Complete the sentence (word length: {})".format(question['length']), 
                                           True, self.colors.WHITE)
        sentence_parts = question['sentence'].split("_____")
        
        # Render sentence with blank
        part1 = self.font_medium.render(sentence_parts[0], True, self.colors.CYAN)
        blank = self.font_medium.render("_____", True, self.colors.YELLOW)
        part2 = self.font_medium.render(sentence_parts[1] if len(sentence_parts) > 1 else "", True, self.colors.CYAN)
        
        # Input box
        input_box = pygame.Rect(300, 350, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_active
        text = ""
        active = True
        
        # Timer animation variables
        timer_width = 400 * (time_remaining / 60)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            
            # Draw everything
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))
            
            # Draw timer bar
            pygame.draw.rect(self.screen, (50, 50, 100), (200, 50, 400, 20))
            pygame.draw.rect(self.screen, (0, 200, 100), (200, 50, timer_width, 20))
            
            self.screen.blit(score_text, (20, 20))
            self.screen.blit(time_text, (self.width - time_text.get_width() - 20, 20))
            self.screen.blit(instruction, (self.width//2 - instruction.get_width()//2, 150))
            
            # Draw sentence with blank
            x_pos = self.width//2 - (part1.get_width() + blank.get_width() + part2.get_width())//2
            self.screen.blit(part1, (x_pos, 250))
            self.screen.blit(blank, (x_pos + part1.get_width(), 250))
            if len(sentence_parts) > 1:
                self.screen.blit(part2, (x_pos + part1.get_width() + blank.get_width(), 250))
            
            # Draw input box
            txt_surface = self.font_medium.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            pygame.draw.rect(self.screen, color, input_box, 2)
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            
            pygame.display.flip()
            self.clock.tick(30)
            
            # Update timer
            new_time_remaining = max(0, time_remaining - 0.03)
            if new_time_remaining <= 0:
                return ""
            time_remaining = new_time_remaining
            timer_width = 400 * (time_remaining / 60)

    def show_feedback(self, message, duration=2):
        start_time = pygame.time.get_ticks()
        
        while pygame.time.get_ticks() - start_time < duration * 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))
            
            feedback = self.font_medium.render(message, True, self.colors.GREEN if "Correct" in message else self.colors.RED)
            self.screen.blit(feedback, (self.width//2 - feedback.get_width()//2, self.height//2))
            
            pygame.display.flip()
            self.clock.tick(30)

    def show_game_over(self, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))
            
            game_over = self.font_large.render("GAME OVER", True, self.colors.RED)
            score_text = self.font_medium.render(f"Your final score: {score}", True, self.colors.YELLOW)
            prompt = self.font_medium.render("Press any key to continue...", True, self.colors.GREEN)
            
            self.screen.blit(game_over, (self.width//2 - game_over.get_width()//2, 200))
            self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 300))
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, 400))
            
            pygame.display.flip()
            self.clock.tick(30)

    def show_victory(self, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))
            
            congrats = self.font_large.render("CONGRATULATIONS!", True, self.colors.GREEN)
            score_text = self.font_medium.render(f"You completed all sentences with a score of {score}", True, self.colors.YELLOW)
            prompt = self.font_medium.render("Press any key to continue...", True, self.colors.GREEN)
            
            self.screen.blit(congrats, (self.width//2 - congrats.get_width()//2, 200))
            self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 300))
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, 400))
            
            pygame.display.flip()
            self.clock.tick(30)

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "1"
                    elif event.key == pygame.K_2:
                        return "2"
                    elif event.key == pygame.K_3:
                        return "3"

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))
            
            title = self.font_large.render("MAIN MENU", True, self.colors.CYAN)
            option1 = self.font_medium.render("1. Start Game", True, self.colors.WHITE)
            option2 = self.font_medium.render("2. View Example Sentences", True, self.colors.WHITE)
            option3 = self.font_medium.render("3. Exit", True, self.colors.WHITE)
            
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            self.screen.blit(option1, (self.width//2 - option1.get_width()//2, 250))
            self.screen.blit(option2, (self.width//2 - option2.get_width()//2, 300))
            self.screen.blit(option3, (self.width//2 - option3.get_width()//2, 350))
            
            pygame.display.flip()
            self.clock.tick(30)

    def show_examples(self, corpus):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 50))
            
            title = self.font_large.render("EXAMPLE SENTENCES", True, self.colors.CYAN)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
            
            y_pos = 120
            for i, sentence in enumerate(corpus[:5], 1):
                text = self.font_small.render(f"{i}. {sentence}", True, self.colors.WHITE)
                self.screen.blit(text, (50, y_pos))
                y_pos += 30
            
            count = self.font_small.render(f"Total sentences in game: {len(corpus)}", True, self.colors.YELLOW)
            prompt = self.font_medium.render("Press any key to continue...", True, self.colors.GREEN)
            
            self.screen.blit(count, (50, y_pos + 20))
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, self.height - 100))
            
            pygame.display.flip()
            self.clock.tick(30)