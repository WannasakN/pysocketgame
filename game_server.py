import random

class GameNumber:
    MAX_ATTEMPTS = 10

    def __init__(self):
        self.answer = random.randint(1, 100)
        self.state = "Start"

    def play(self, user_input):
        if self.state == "Start":
            self.state = "Play"
        elif self.state in ["TooHigh", "TooLow"]:
            self.state = "Play"

        if self.MAX_ATTEMPTS == 0 :
            return 'You exceeded the maximum number of attempts. Game over.'
        
        elif user_input == self.answer:
            self.state = "CorrectAnswer"
            return "Correct! \nGame End , See you next time."

        elif user_input > self.answer:
            self.state = "TooHigh"
            self.MAX_ATTEMPTS -= 1
            return "It's less than that."
        
        elif user_input < self.answer:
            self.state = "TooLow"
            self.MAX_ATTEMPTS -= 1
            return "It's more than that."