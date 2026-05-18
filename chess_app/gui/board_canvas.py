import tkinter as tk
import chess

from chess_analyzer.chess_app.constants import (
    LIGHT_SQUARE,
    DARK_SQUARE,
    SQUARE_SIZE,
    BOARD_WIDTH,
    BOARD_HEIGHT,
)


class BoardCanvas(tk.Canvas):
    def __init__(self, parent, app):
        super().__init__(parent, width=BOARD_WIDTH, height=BOARD_HEIGHT)

        self.app = app

        self.square_size = SQUARE_SIZE

        self.draw_board()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x1 = self.square_size * col
                y1 = self.square_size * row
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                colour = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE

                self.create_rectangle(x1, y1, x2, y2, fill=colour)

    def redraw_board(self, board):
        self.delete("piece")
        self.delete("arrow")
        self.delete("move_icon")  

        if board is None:
            return

        square_size = self.square_size

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece:
                row = 7 - square // 8
                col = square % 8
                x = col * square_size
                y = row * square_size
                self.create_image(
                    x,
                    y,
                    image=self.app.pieces[piece.symbol()],
                    anchor="nw",
                    tags="piece",
                )

    def draw_best_move_arrow(self, best_move):
        self.delete("arrow")

        from_square = best_move.from_square
        to_square = best_move.to_square

        square_size = self.square_size

        from_row = 7 - from_square // 8
        from_col = from_square % 8
        to_row = 7 - to_square // 8
        to_col = to_square % 8

        x1 = from_col * square_size + square_size // 2
        y1 = from_row * square_size + square_size // 2
        x2 = to_col * square_size + square_size // 2
        y2 = to_row * square_size + square_size // 2

        self.create_line(
            x1, y1, x2, y2, arrow="last", width=4, fill="red", tags="arrow"
        )

    def draw_move_icon(self, move, classification):
        self.delete("move_icon")  

        if not classification:
            return

        icon = self.app.move_icons.get(classification)
        if icon is None:
            return

        square = move.to_square
        row = 7 - square // 8
        col = square % 8

        x = col * SQUARE_SIZE + 72
        y = row * SQUARE_SIZE + 4

        self.create_image(x, y, image=icon, anchor="nw", tags="move_icon")
