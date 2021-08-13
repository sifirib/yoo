import random
import discord
from shared import words
# from User import User
from databases.model import *

class Hangman(object):
    hangman_words = {i: words[i] for i in range(0, len(words))}

    def start_game(self, user):
        self.user = user
        self.user_ = get_user(user.id)
        self.chosen_word = ""
        self.guessed_letters = ""
        self.incorrect_letters = ["Incorrect letters: "]
        self.remaining_guesses = 8
        self.has_ended = False
        self.has_won = False
        random.seed()
        key = random.randint(1, len(self.hangman_words))
        self.chosen_word = self.hangman_words[key].lower()
        self.guessed_letters = "_" * len(self.chosen_word)
        self.contains_guess = False

        if not self.user_:
             self.user_ = Person(self.user.id, 1000, 0).save()

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

        if self.has_ended and self.has_won:
            self.user_.coin = (self.user_.coin + 10 * len(self.chosen_word))
            message += '\n **__You won! You correctly guessed__** ' + f'`{self.chosen_word}`'

        elif self.has_ended and not self.has_won:
            self.user_.coin = (self.user_.coin - 10 * len(self.chosen_word))
            message += '\n **__You lost! The correct word was__** ' + f'`{self.chosen_word}`'
        
        self.user_.update()
        db.commit()

        message += f"\n`You have {self.user_.coin} coins..`"
        return message
    

    def guess(self, message):
        args = message.split(' ')
        guess = ""
        self.contains_guess = False

        if len(args) > 1:
            guess = args[1].lower()
        if len(guess) > 1:
            if guess == self.chosen_word:
                self.guessed_letters = self.chosen_word
                self.contains_guess = True
                self.has_ended = True
                self.has_won = True
            else:
                self.remaining_guesses -= 1
        else:

            for i in range(0, len(self.chosen_word)):
                if guess[0] == self.chosen_word[i]:
                    self.guessed_letters = self.guessed_letters[:i] + guess[0] + self.guessed_letters[i + 1:]
                    self.contains_guess = True
            if not self.contains_guess and self.remaining_guesses > 0:
                self.remaining_guesses -= 1
                if guess[0] not in self.incorrect_letters:
                    self.incorrect_letters.append(guess[0])

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
            if self.remaining_guesses == 0:
                self.has_ended = True
                self.has_won = False



    
    def create_embed(self, description):
        
        embed = discord.Embed(title="Hangman", url="https://github.com/sifirib/discord_bot", description=f"```{description}```")
        # embed.set_author(name="author name", url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwS70r6aZEg6-wofSf66x7MU7FiZSEFSOIQA&usqp=CAU", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwS70r6aZEg6-wofSf66x7MU7FiZSEFSOIQA&usqp=CAU")
        embed.add_field(name=self.get_game_status(), value=", ".join(self.incorrect_letters), inline=True)
        # embed.add_field(name="fileld name2", value="field value2", inline=True)
        # embed.set_footer(text="footer text")
        gif = ""
        if self.has_ended:
            if self.has_won:
                gif = "https://media.tenor.com/images/2d126625a12ea0a819f3fd9d9bfee728/tenor.gif"
            else:
                gif = "https://media.tenor.com/images/b7c14f66c154f1e823b638eafd4b9cca/tenor.gif"
        else:
            gif = "https://media.tenor.com/images/d536a9d9cbf3b69a745b58e9b68f3cfb/tenor.gif"
        embed.set_thumbnail(url=gif)

            

        return embed
