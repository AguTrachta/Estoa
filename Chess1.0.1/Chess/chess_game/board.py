from .Pieces import *
from .constants import *

class Board:
    def __init__(self, Width, Height, Rows, Cols, Square):
        self.Width = Width
        self.Height = Height
        self.Square = Square
        self.Rows = Rows
        self.Cols = Cols
        self.Board = []
        self.create_Board()
        self.promotion_choice = None

    def create_Board(self):
        for row in range(self.Rows):
            self.Board.append([0 for _ in range(self.Cols)])
            for col in range(self.Cols):
                if row == 1:
                    self.Board[row][col] = Pawn(self.Square, Black_Pawn, Black, "Pawn", row, col)
                if row == 6:
                    self.Board[row][col] = Pawn(self.Square, White_Pawn, White, "Pawn", row, col)

                if row == 0:
                    if col == 0 or col == 7:
                        self.Board[row][col] = Rook(self.Square, Black_Rook, Black, "Rook", row, col)
                    if col == 1 or col == 6:
                        self.Board[row][col] = Knight(self.Square, Black_Knight, Black, "Knight", row, col)
                    if col == 2 or col == 5:
                        self.Board[row][col] = Bishop(self.Square, Black_Bishop, Black, "Bishop", row, col)
                    if col == 3:
                        self.Board[row][col] = Queen(self.Square, Black_Queen, Black, "Queen", row, col)
                    if col == 4:
                        self.Board[row][col] = King(self.Square, Black_King, Black, "King", row, col)

                if row == 7:
                    if col == 0 or col == 7:
                        self.Board[row][col] = Rook(self.Square, White_Rook, White, "Rook", row, col)
                    if col == 1 or col == 6:
                        self.Board[row][col] = Knight(self.Square, White_Knight, White, "Knight", row, col)
                    if col == 2 or col == 5:
                        self.Board[row][col] = Bishop(self.Square, White_Bishop, White, "Bishop", row, col)
                    if col == 3:
                        self.Board[row][col] = Queen(self.Square, White_Queen, White, "Queen", row, col)
                    if col == 4:
                        self.Board[row][col] = King(self.Square, White_King, White, "King", row, col)

    def get_piece(self, row, col):
        return self.Board[row][col]

    def move(self, piece, row, col):
        self.Board[piece.row][piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
        piece.piece_move(row, col)
        piece.first_move = False

        if piece.type == "Pawn":
            if (piece.color == White and row == 0) or (piece.color == Black and row == 7):
                self.promotion_choice = piece

    def remove_piece(self, piece):
        self.Board[piece.row][piece.col] = 0

    def promote_pawn(self, choice):
        if self.promotion_choice:
            row, col = self.promotion_choice.row, self.promotion_choice.col
            color = self.promotion_choice.color

            if choice == "Queen":
                self.Board[row][col] = Queen(self.Square, White_Queen if color == White else Black_Queen, color, "Queen", row, col)
            elif choice == "Rook":
                self.Board[row][col] = Rook(self.Square, White_Rook if color == White else Black_Rook, color, "Rook", row, col)
            elif choice == "Bishop":
                self.Board[row][col] = Bishop(self.Square, White_Bishop if color == White else Black_Bishop, color, "Bishop", row, col)
            elif choice == "Knight":
                self.Board[row][col] = Knight(self.Square, White_Knight if color == White else Black_Knight, color, "Knight", row, col)

            self.promotion_choice = None

