import json
import random
import os
from pathlib import Path
from time import sleep

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class NGramGame:
    def __init__(self):
        self.score = 0
        self.user_answers = []
        self.correct_answers = []
        self.difficulty = "medium"
        self.questions = self.load_questions()
        self.current_question_index = 0
        self.hints_remaining = 3

    def load_questions(self):
        questions = {
            "easy": [
                {"sentence": "I love an animal that", "length": 4, "options": ["goat", "bear", "lion", "wolf"], "hint": "Common pet or wild animal"},
                {"sentence": "The color of sky is", "length": 4, "options": ["blue", "gray", "pink", "teal"], "hint": "Typically seen on clear days"},
                {"sentence": "I drink a glass of", "length": 5, "options": ["water", "juice", "milk", "soda"], "hint": "Essential for life"},
                {"sentence": "We sleep on a", "length": 3, "options": ["bed", "mat", "cot", "rug"], "hint": "Furniture for resting"},
                {"sentence": "The sun is very", "length": 3, "options": ["hot", "big", "far", "red"], "hint": "Opposite of cold"},
                {"sentence": "Apples are usually", "length": 3, "options": ["red", "sour", "soft", "tiny"], "hint": "Common color"},
                {"sentence": "I write with a", "length": 3, "options": ["pen", "paw", "rod", "pin"], "hint": "Common writing tool"},
                {"sentence": "Birds can", "length": 3, "options": ["fly", "run", "dig", "swim"], "hint": "What makes them special"},
                {"sentence": "Winter is", "length": 4, "options": ["cold", "warm", "dark", "long"], "hint": "Opposite of summer"},
                {"sentence": "My shoes are", "length": 3, "options": ["new", "old", "red", "big"], "hint": "Opposite of old"}
            ],
            "medium": [
                {"sentence": "The weather today is", "length": 3, "options": ["hot", "wet", "dry", "sun"], "hint": "Describes temperature"},
                {"sentence": "She works as a", "length": 6, "options": ["doctor", "nurse", "artist", "writer"], "hint": "Medical professional"},
                {"sentence": "We traveled by", "length": 3, "options": ["car", "bus", "air", "sea"], "hint": "Common vehicle"},
                {"sentence": "The movie was", "length": 4, "options": ["long", "boring", "funny", "scary"], "hint": "Duration description"},
                {"sentence": "I need to buy", "length": 4, "options": ["milk", "bread", "eggs", "meat"], "hint": "Dairy product"},
                {"sentence": "The book was", "length": 5, "options": ["great", "short", "bland", "thick"], "hint": "Positive adjective"},
                {"sentence": "We played", "length": 6, "options": ["soccer", "tennis", "puzzle", "cards"], "hint": "Team sport"},
                {"sentence": "The music is", "length": 4, "options": ["loud", "soft", "fast", "slow"], "hint": "Volume description"},
                {"sentence": "My phone is", "length": 5, "options": ["black", "broken", "new", "small"], "hint": "Color option"},
                {"sentence": "The cake tastes", "length": 5, "options": ["sweet", "salty", "bitter", "sour"], "hint": "Dessert characteristic"}
            ],
            "hard": [
                {"sentence": "He studies quantum", "length": 8, "options": ["physics", "mechanics", "chemistry", "biology"], "hint": "Advanced physics"},
                {"sentence": "The conference was about", "length": 11, "options": ["technology", "innovation", "marketing", "economics"], "hint": "Tech-related"},
                {"sentence": "Her specialization is", "length": 9, "options": ["neurology", "cardiology", "pediatrics", "oncology"], "hint": "Medical field"},
                {"sentence": "The novel explores", "length": 11, "options": ["existentialism", "romanticism", "modernism", "realism"], "hint": "Philosophical theme"},
                {"sentence": "The algorithm uses", "length": 13, "options": ["machinelearning", "blockchain", "cryptography", "biometrics"], "hint": "AI technology"},
                {"sentence": "The research focuses on", "length": 10, "options": ["genetics", "climate", "behavior", "disease"], "hint": "Biological science"},
                {"sentence": "The artist works with", "length": 8, "options": ["acrylics", "watercolor", "charcoal", "pastels"], "hint": "Painting medium"},
                {"sentence": "The expedition explored", "length": 9, "options": ["Antarctica", "Amazon", "Sahara", "Himalayas"], "hint": "Cold continent"},
                {"sentence": "The orchestra played", "length": 7, "options": ["symphony", "concerto", "sonata", "opera"], "hint": "Musical composition"},
                {"sentence": "The debate covered", "length": 11, "options": ["immigration", "healthcare", "education", "taxation"], "hint": "Political topic"}
            ]
        }
        return questions

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}N-GRAM WORD PREDICTION GAME{Colors.RESET}")
        print(f"{Colors.YELLOW}Difficulty: {self.difficulty.capitalize()}{Colors.RESET}")
        print(f"{Colors.BLUE}Score: {self.score}/10 | Hints: {self.hints_remaining}{Colors.RESET}\n")

    def play_game(self):
        self.print_header()
        questions = self.questions[self.difficulty]
        
        for i, question in enumerate(questions, 1):
            self.current_question_index = i-1
            self.print_question(question, i)
            
            while True:
                user_input = input(f"{Colors.GREEN}Your answer (or 'hint'): {Colors.RESET}").strip().lower()
                
                if user_input == "hint":
                    self.use_hint(question)
                    continue
                    
                if self.check_answer(user_input, question):
                    break
        
        self.show_answer_sheet()

    def print_question(self, question, q_num):
        self.print_header()
        print(f"{Colors.BOLD}Question {q_num}:{Colors.RESET}")
        print(f"{question['sentence']} {'[_]' * question['length']}\n")
        print(f"Options: {', '.join(question['options'])}")

    def use_hint(self, question):
        if self.hints_remaining > 0:
            self.hints_remaining -= 1
            print(f"\n{Colors.CYAN}Hint: {question['hint']}{Colors.RESET}\n")
        else:
            print(f"\n{Colors.RED}No hints remaining!{Colors.RESET}\n")

    def check_answer(self, user_input, question):
        options = [opt.lower() for opt in question['options']]
        if user_input in options:
            correct_answer = random.choice(question['options'])
            self.correct_answers.append(correct_answer)
            self.user_answers.append(user_input)
            
            if user_input == correct_answer.lower():
                self.score += 1
                print(f"\n{Colors.GREEN}Correct!{Colors.RESET}")
            else:
                print(f"\n{Colors.RED}Incorrect!{Colors.RESET}")
            
            input("\nPress Enter to continue...")
            return True
        else:
            print(f"{Colors.RED}Invalid choice. Please select from the given options.{Colors.RESET}")
            return False

    def show_answer_sheet(self):
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.UNDERLINE}ANSWER SHEET{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Final Score: {self.score}/10{Colors.RESET}\n")
        
        questions = self.questions[self.difficulty]
        for i in range(10):
            q = questions[i]
            user_answer = self.user_answers[i]
            correct_answer = self.correct_answers[i]
            
            print(f"{Colors.BOLD}Q{i+1}: {q['sentence']} {correct_answer}{Colors.RESET}")
            print(f"Your answer: {Colors.GREEN if user_answer == correct_answer.lower() else Colors.RED}{user_answer}{Colors.RESET}")
            print(f"Options: {', '.join(q['options'])}")
            print("-" * 50)
        
        input("\nPress Enter to return to main menu...")

    def set_difficulty(self):
        self.clear_screen()
        print(f"{Colors.BOLD}SELECT DIFFICULTY{Colors.RESET}\n")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        
        while True:
            choice = input("\nEnter your choice (1-3): ")
            if choice == "1":
                self.difficulty = "easy"
                break
            elif choice == "2":
                self.difficulty = "medium"
                break
            elif choice == "3":
                self.difficulty = "hard"
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")

    def main_menu(self):
        while True:
            self.clear_screen()
            print(f"{Colors.CYAN}{Colors.BOLD}MAIN MENU{Colors.RESET}\n")
            print("1. Start Game")
            print("2. Change Difficulty")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                self.score = 0
                self.user_answers = []
                self.correct_answers = []
                self.hints_remaining = 3
                self.play_game()
            elif choice == "2":
                self.set_difficulty()
            elif choice == "3":
                print(f"\n{Colors.YELLOW}Thanks for playing!{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
                sleep(1)

if __name__ == "__main__":
    game = NGramGame()
    game.main_menu()