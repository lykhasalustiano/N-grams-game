import random
import time

class CrosswordGame:
    """Manages the state and logic of the crossword game."""
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.base_time = 60 # Default base time
        self.time_remaining = self.base_time
        self.time_multiplier = 1.0 # Speed multiplier for timer
        self.start_time = 0
        self.last_update = 0
        self.round_number = 0
        self.max_rounds = 10
        self.difficulty = "easy"
        self.current_question = None
        self.used_questions = []

        # Difficulty-based sentences
        self.sentences = {
            "easy": [
                ("the cat is very", "cute", 4),
                ("i like to eat", "pizza", 5),
                ("the sun is", "bright", 6),
                ("dogs are very", "loyal", 5),
                ("water is", "wet", 3),
                ("ice is", "cold", 4),
                ("fire is", "hot", 3),
                ("grass is", "green", 5),
                ("snow is", "white", 5),
                ("the book is", "good", 4),
                ("music sounds", "nice", 4),
                ("flowers smell", "sweet", 5),
                ("the car is", "fast", 4),
                ("birds can", "fly", 3),
                ("fish can", "swim", 4)
            ],
            "medium": [
                ("the weather today is quite", "pleasant", 8),
                ("students need to study", "carefully", 9),
                ("technology is advancing", "rapidly", 7),
                ("exercise helps maintain", "health", 6),
                ("reading books expands", "knowledge", 9),
                ("teamwork requires good", "communication", 13),
                ("cooking requires", "patience", 8),
                ("learning languages takes", "practice", 8),
                ("friendship brings", "happiness", 9),
                ("travel broadens our", "perspective", 11),
                ("art expresses human", "creativity", 10),
                ("science explains natural", "phenomena", 9),
                ("music evokes strong", "emotions", 8),
                ("nature provides", "inspiration", 11),
                ("dreams motivate", "achievement", 11)
            ],
            "hard": [
                ("the philosopher contemplated existential", "questions", 9),
                ("quantum mechanics defies intuitive", "understanding", 13),
                ("biodiversity conservation requires immediate", "action", 6),
                ("artificial intelligence demonstrates remarkable", "capabilities", 12),
                ("sustainable development needs global", "cooperation", 11),
                ("psychological research reveals human", "complexity", 10),
                ("archaeological discoveries provide historical", "evidence", 8),
                ("neuroscience explores brain", "functionality", 13),
            ]
        }
        self.all_questions = {}
        for diff, q_list in self.sentences.items():
            self.all_questions[diff] = [
                {'sentence': s, 'answer': a, 'length': l} for s, a, l in q_list
            ]
        
    def set_difficulty(self, difficulty):
        """Sets the game difficulty and associated timer."""
        self.difficulty = difficulty
        if difficulty == "easy":
            self.base_time = 60
        elif difficulty == "medium":
            self.base_time = 45
        elif difficulty == "hard":
            self.base_time = 30
        self.time_remaining = self.base_time
    
    def get_new_question(self):
        """
        Gets a new, unused question for the current round.
        Generates 3 random wrong options as well.
        """
        if self.round_number >= self.max_rounds or self.lives <= 0:
            return None
        
        available_questions = [q for q in self.all_questions[self.difficulty] if q not in self.used_questions]
        
        if not available_questions:
            return None # No more questions
        
        question = random.choice(available_questions)
        self.used_questions.append(question)
        self.current_question = question
        self.round_number += 1

        # Generate wrong options
        all_answers = [q['answer'] for q in self.all_questions[self.difficulty]]
        all_answers.remove(question['answer'])
        wrong_options = random.sample(all_answers, 3)

        options = [question['answer']] + wrong_options
        random.shuffle(options)
        
        self.current_question['options'] = options
        
        # Reset and start timer
        self.time_remaining = self.base_time
        self.start_time = time.time()
        self.last_update = self.start_time

        return self.current_question

    def update_timer(self):
        """Updates the timer based on elapsed time and multiplier."""
        current_time = time.time()
        elapsed = current_time - self.last_update
        self.time_remaining -= elapsed * self.time_multiplier
        self.last_update = current_time
        return self.time_remaining

    def check_answer(self, selected_option_index):
        """Checks if the user's selected answer is correct."""
        if selected_option_index == -1:
            # Handle time's up scenario
            self.lives -= 1
            self.time_multiplier = 2.0
            correct_word = self.current_question['answer']
            message = f"Time's up! The correct word was '{correct_word.upper()}'! !Your timer is now faster!"
            return False, message
        
        selected_answer = self.current_question['options'][selected_option_index]
        correct_answer = self.current_question['answer']

        if selected_answer == correct_answer:
            self.score += 1
            self.time_remaining += 30
            self.time_multiplier = 1.0
            return True, "Correct! Your timer is back to normal speed and you gained 30 seconds!"
        else:
            self.lives -= 1
            self.time_multiplier = 2.0
            correct_word = self.current_question['answer']
            message = f"Wrong! The correct word was '{correct_word.upper()}'! !Your timer is now faster!"
            return False, message
            
    def is_game_over(self):
        """Checks if the game has ended."""
        return self.round_number >= self.max_rounds or self.lives <= 0

    def get_final_message(self):
        """Generates the final message based on the game outcome."""
        if self.round_number >= self.max_rounds and self.lives > 0:
            return "CONGRATULATIONS! YOU WON THE CHALLENGE!"
        else:
            return "GAME OVER!"