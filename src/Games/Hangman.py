import random

class Hangman(object):
    # chosen_word = ""
    # guessed_letters = ""
    # remaining_guesses = 6
    words = {
        1: 'abc',
        2: 'abcdef',
        3: 'apple',
        4: 'yooo',
        5: 'python',
        6: 'oleybe'}
    # has_ended = False
    # has_won = False

    def start_game(self):
        self.chosen_word = ""
        self.guessed_letters = ""
        self.remaining_guesses = 6
        self.has_ended = False
        self.has_won = False
        random.seed()
        key = random.randint(1, len(self.words))
        self.chosen_word = self.words[key]
        # for i in range(0, len(self.chosen_word)):
        #     new_string += "_"
        self.guessed_letters = "_" * len(self.chosen_word)

    def get_game_status(self):
        # return a string containing the current game status and if
        # the player has won or not
        message = ""

        if not self.has_ended:
            # print each letter followed by a space
            letters = ""
            for i in range(0, len(self.guessed_letters)):
                letters += self.guessed_letters[i] + ' '
            message = f'{self.remaining_guesses} guesses left \n`{letters}`'
            # message += letters

        if self.has_ended and self.has_won:
            message += '\n You won! You correctly guessed ' + f'`{self.chosen_word}`'
        elif self.has_ended and not self.has_won:
            message += '\n You lost! The correct word was ' + f'`{self.chosen_word}`'

        return message
    
    def guess(self, message):
        args = message.split(' ')
        guess = ""
        contains_guess = False

        if len(args) > 2:
            guess = args[2]

        for i in range(0, len(self.chosen_word)):
            if guess[0] == self.chosen_word[i]:
                self.guessed_letters = self.guessed_letters[:i] + guess[0] + self.guessed_letters[i + 1:]
                contains_guess = True
        if not contains_guess:
            self.remaining_guesses -= 1

        # check for letters that haven't been guessed
        unguessed_letters = False
        for letter in self.guessed_letters:
            if letter == '_':
                unguessed_letters = True

        # player has won the game
        if not unguessed_letters:
            self.has_ended = True
            self.has_won = True

        # no more guesses, so the player has lost
        if self.remaining_guesses < 0:
            self.has_ended = True
            self.has_won = False