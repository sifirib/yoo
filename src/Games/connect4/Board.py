from enum import Enum


class Board:
    def __init__(self, height=6, width=7):
        self.width = width
        self.height = height
        self.board = [[Piece.EMPTY for _ in range(width)] for _ in range(height)]  # 6 x 7

    def getPiece(self, x, y):
        return self.board[y][x]

    def addPiece(self, col, peice):
        for i in range(self.height):
            if self.board[self.height - i - 1][col] == Piece.EMPTY:
                self.board[self.height - i - 1][col] = peice
                return col, self.height - i - 1

        return False

    def checkWin(self, x, y, piece):
        """
        Check if the move is a winning move
        :param x:
        :param y:
        :return:
        """

        count = 0

        # Check rows
        for i in range(max(x - 4, 0), min(x + 4, self.width)):
            if self.board[y][i] == piece:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True

        # Check cols
        for i in range(max(y - 4, 0), min(y + 4, self.height)):
            if self.board[i][x] == piece:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True

        # Check diag
        drc = 0
        dlc = 0

        for i in range(-3, 4):
            if x + i < self.width and y + i < self.height and x + i >= 0 and y + i >= 0 and self.board[y + i][
                        x + i] == piece:
                drc += 1
            else:
                drc = 0

            if x + i < self.width and y - i < self.height and x + i >= 0 and y - i >= 0 and self.board[y - i][
                        x + i] == piece:
                dlc += 1
            else:
                dlc = 0

            if dlc >= 4 or drc >= 4:
                return True

        return False

    def __repr__(self):
        return "\n".join((["|" + "|".join(
            ["O" if y == Piece.RED else ("X" if y == Piece.BLACK else "_") for y in x]) + "|" for x in
                           self.board])) + "\n"


class Piece(Enum):
    EMPTY = 0
    RED = 1
    BLACK = 2
