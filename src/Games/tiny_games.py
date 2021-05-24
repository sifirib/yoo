from random import randint


class Game(object):

    @staticmethod
    def roll_dice():

        return randint(0, 6)
