from connect4.Board import Board, Piece
from PIL import Image, ImageDraw

from io import BytesIO


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()

    def move(self, column):
        if self.turn == 0:
            piece = Piece.RED
        else:
            piece = Piece.BLACK

        coords = self.board.addPiece(column, piece)

        # Invalid move
        if not coords:
            return -1

        # Someone won
        if self.board.checkWin(coords[0], coords[1], piece):
            return 1

        self.turn = (self.turn + 1) % 2

        # Next turn
        return 0

    def __repr__(self):
        return self.board.__repr__()

    def __str__(self):
        return self.__repr__()

    def generateImageBoard(self, color1="red", color2="black"):
        im = Image.new("RGB", (256, 220), "white")
        draw = ImageDraw.Draw(im)

        diameter = 32
        padding = 4
        margin = 4

        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.board.getPiece(i, j) == Piece.RED:
                    color = color1
                    outline = 'red'
                elif self.board.getPiece(i, j) == Piece.BLACK:
                    color = color2
                    outline = 'black'
                else:
                    color = 'grey'
                    outline = "black"

                draw.ellipse((margin + (diameter + padding) * i, margin + (diameter + padding) * j,
                              margin + (diameter + padding) * i + diameter,
                              margin + (diameter + padding) * j + diameter), fill=color,
                             outline=outline)

        return im


if __name__ == "__main__":
    game = Game()

    print(game.board)

    game.move(0)
    game.move(3)
    game.move(1)
    game.move(1)
    game.move(2)
    game.move(2)
    game.move(0)
    game.move(1)
    game.move(0)
    print(game.move(0))

    game.generateImageBoard("#0F0").show()

    pass
