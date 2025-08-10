import math
import random
import os
from collections import defaultdict
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
        self.current_question_index = 0
        self.hints_remaining = 3
        
        self.corpus = [
            "the quick brown fox jumps over the lazy dog",
            "the quick brown bear sleeps",
            "the brown fox eats apple",
            "the quick break has jumped over the lazy edge",
            "the quick break has dropped",
            "the quick break has stopped"
        ]
        self.unigrams = defaultdict(int)
        self.bigrams = defaultdict(int)
        self.trigrams = defaultdict(int)
        self.vocab = set()
        self.build_ngram_models()
        self.questions = self.generate_questions()

    def build_ngram_models(self):
        """Build n-gram counts from corpus (as shown in your images)"""
        for sentence in self.corpus:
            tokens = ['<s>'] + sentence.split() + ['</s>']
          
            self.vocab.update(tokens)
            # Unigrams
            for token in tokens:
                self.unigrams[token] += 1
            # Bigrams
            for i in range(len(tokens)-1):
                self.bigrams[(tokens[i], tokens[i+1])] += 1
            # Trigrams
            for i in range(len(tokens)-2):
                self.trigrams[(tokens[i], tokens[i+1], tokens[i+2])] += 1

    def calculate_probability(self, context, word):
        """Calculate probability using Markov assumption and MLE (from your images)"""
        if len(context) == 2:  # Trigram
            count = self.trigrams.get((context[0], context[1], word), 0) + 1
            denominator = self.bigrams.get((context[0], context[1]), 0) + len(self.vocab)
            return count / denominator if denominator else 0
        elif len(context) == 1:  # Bigram
            count = self.bigrams.get((context[0], word), 0) + 1
            denominator = self.unigrams.get(context[0], 0) + len(self.vocab)
            return count / denominator if denominator else 0
        else:  # Unigram
            return (self.unigrams.get(word, 0) / sum(self.unigrams.values()))

    def log_probability(self, context, word):
        """Log probability to avoid underflow (as shown in your images)"""
        prob = self.calculate_probability(context, word)
        return math.log(prob) if prob > 0 else float('-inf')

    def generate_questions(self):
        """Generate questions based on actual n-gram probabilities"""
        questions = {"easy": [], "medium": [], "hard": []}
        vocab_list = list(self.vocab - {'<s>', '</s>'})
        
        for difficulty in questions:
            for _ in range(10):
                # Select random context from corpus
                sentence = random.choice(self.corpus)
                tokens = sentence.split()
                if len(tokens) < 2:
                    continue
                
                if difficulty == "easy":
                    # Bigram questions
                    context_pos = random.randint(0, len(tokens)-2)
                    context = tokens[context_pos:context_pos+1]
                    correct_next = tokens[context_pos+1]
                    ngram_type = "bigram"
                elif difficulty == "medium":
                    # Trigram questions
                    context_pos = random.randint(0, len(tokens)-3)
                    context = tokens[context_pos:context_pos+2]
                    correct_next = tokens[context_pos+2]
                    ngram_type = "trigram"
                else:  # hard
                    # Mixed with log probabilities
                    if random.random() > 0.5:
                        context_pos = random.randint(0, len(tokens)-2)
                        context = tokens[context_pos:context_pos+1]
                        correct_next = tokens[context_pos+1]
                        ngram_type = "bigram (log)"
                    else:
                        context_pos = random.randint(0, len(tokens)-3)
                        context = tokens[context_pos:context_pos+2]
                        correct_next = tokens[context_pos+2]
                        ngram_type = "trigram (log)"
                
                # Get probable options
                options = [correct_next]
                probs = {}
                for word in vocab_list:
                    if word not in context and word != correct_next:
                        if "log" in ngram_type:
                            probs[word] = self.log_probability(context, word)
                        else:
                            probs[word] = self.calculate_probability(context, word)
                
                # Add top 3 probable alternatives
                top_words = sorted(probs.items(), key=lambda x: -x[1])[:3]
                options.extend([w for w, _ in top_words])
                
                # Ensure we have 4 options
                while len(options) < 4 and len(vocab_list) > len(options):
                    word = random.choice(vocab_list)
                    if word not in options and word not in context:
                        options.append(word)
                
                random.shuffle(options)
                
                questions[difficulty].append({
                    "sentence": " ".join(context),
                    "length": len(correct_next),
                    "options": options,
                    "hint": f"{ngram_type} from: '{sentence}'",
                    "correct": correct_next,
                    "context": context,
                    "ngram_type": ngram_type
                })
        return questions

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}N-GRAM WORD PREDICTION GAME{Colors.RESET}")
        print(f"{Colors.YELLOW}Difficulty: {self.difficulty.capitalize()}{Colors.RESET}")
        print(f"{Colors.BLUE}Score: {self.score}/10 | Hints: {self.hints_remaining}{Colors.RESET}\n")
        print(f"{Colors.BOLD}Current Corpus:{Colors.RESET}")
        for i, sent in enumerate(self.corpus[:3], 1):
            print(f"{i}. {sent}")
        print()

    def play_game(self):
        self.print_header()
        questions = self.questions[self.difficulty]
        
        for i, question in enumerate(questions, 1):
            self.current_question_index = i-1
            self.print_question(question, i)
            
            while True:
                user_input = input(f"{Colors.GREEN}Your answer (or 'hint'/'theory'): {Colors.RESET}").strip().lower()
                
                if user_input == "hint":
                    self.use_hint(question)
                    continue
                elif user_input == "theory":
                    self.explain_theory(question)
                    continue
                    
                if self.check_answer(user_input, question):
                    break
        
        self.show_answer_sheet()

    def print_question(self, question, q_num):
        self.print_header()
        print(f"{Colors.BOLD}Question {q_num}:{Colors.RESET}")
        print(f"Given the context: {Colors.CYAN}'{question['sentence']}'{Colors.RESET}")
        print(f"Predict the next word (length: {question['length']} letters)\n")
        print(f"Options: {', '.join(question['options'])}")
        print(f"\n{Colors.YELLOW}Type 'theory' to see NLP concepts for this question{Colors.RESET}")

    def use_hint(self, question):
        if self.hints_remaining > 0:
            self.hints_remaining -= 1
            print(f"\n{Colors.CYAN}Hint: {question['hint']}{Colors.RESET}\n")
        else:
            print(f"\n{Colors.RED}No hints remaining!{Colors.RESET}\n")

    def explain_theory(self, question):
        print(f"\n{Colors.BOLD}Relevant NLP Concepts:{Colors.RESET}")
        print(f"- {Colors.YELLOW}Markov Assumption:{Colors.RESET} Probability depends only on previous {'1' if len(question['context'])==1 else '2'} word(s)")
        
        if "log" in question['ngram_type']:
            print(f"- {Colors.YELLOW}Log Probabilities:{Colors.RESET} Used to avoid underflow in multiplication")
            print(f"  Original: {question['context']} → {question['correct']}")
            print(f"  Calculation: log(p) = {self.log_probability(question['context'], question['correct']):.2f}")
        else:
            print(f"- {Colors.YELLOW}Maximum Likelihood Estimation:{Colors.RESET}")
            print(f"  P({question['correct']}|{','.join(question['context'])}) = {self.calculate_probability(question['context'], question['correct']):.2f}")
        
        print(f"- {Colors.YELLOW}N-gram Type:{Colors.RESET} {question['ngram_type'].upper()}")
        input("\nPress Enter to continue...")
        self.print_question(question, self.current_question_index+1)

    def check_answer(self, user_input, question):
        options = [opt.lower() for opt in question['options']]
        if user_input in options:
            correct_answer = question['correct']
            self.correct_answers.append(correct_answer)
            self.user_answers.append(user_input)
            
            if user_input == correct_answer.lower():
                self.score += 1
                print(f"\n{Colors.GREEN}Correct!{Colors.RESET}")
                prob = (self.log_probability if "log" in question['ngram_type'] else self.calculate_probability)(question['context'], correct_answer)
                print(f"Probability: {prob:.4f}{' (log)' if 'log' in question['ngram_type'] else ''}")
            else:
                print(f"\n{Colors.RED}Incorrect!{Colors.RESET} Correct was '{correct_answer}'")
                print(f"Your answer '{user_input}' probability: {self.calculate_probability(question['context'], user_input):.4f}")
            
            input("\nPress Enter to continue...")
            return True
        else:
            print(f"{Colors.RED}Invalid choice. Please select from: {', '.join(question['options'])}{Colors.RESET}")
            return False

    def show_answer_sheet(self):
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.UNDERLINE}ANSWER SHEET{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Final Score: {self.score}/10{Colors.RESET}\n")
        
        questions = self.questions[self.difficulty]
        for i in range(10):
            q = questions[i]
            user_answer = self.user_answers[i]
            correct_answer = q['correct']
            
            print(f"{Colors.BOLD}Q{i+1}: After '{q['sentence']}', the correct word is: {correct_answer}{Colors.RESET}")
            print(f"Your answer: {Colors.GREEN if user_answer == correct_answer.lower() else Colors.RED}{user_answer}{Colors.RESET}")
            print(f"Probability: {self.calculate_probability(q['context'], correct_answer):.4f} ({q['ngram_type']})")
            print(f"Options: {', '.join(q['options'])}")
            print("-" * 60)
        
        input("\nPress Enter to return to main menu...")

    def set_difficulty(self):
        self.clear_screen()
        print(f"{Colors.BOLD}SELECT DIFFICULTY{Colors.RESET}\n")
        print("1. Easy (Bigrams)")
        print("2. Medium (Trigrams)")
        print("3. Hard (Mixed with Log Probabilities)")
        
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
            print("3. View Corpus")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.score = 0
                self.user_answers = []
                self.correct_answers = []
                self.hints_remaining = 3
                self.play_game()
            elif choice == "2":
                self.set_difficulty()
            elif choice == "3":
                self.view_corpus()
            elif choice == "4":
                print(f"\n{Colors.YELLOW}Thanks for playing!{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
                sleep(1)

    def view_corpus(self):
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.UNDERLINE}CURRENT CORPUS{Colors.RESET}\n")
        for i, sentence in enumerate(self.corpus, 1):
            print(f"{i}. {sentence}")
        print(f"\n{Colors.YELLOW}Vocabulary size: {len(self.vocab)}{Colors.RESET}")
        input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    game = NGramGame()
    game.main_menu()
