# board.py


from .Pieces import *
from .constants import *
import pygame


class newBoard:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Width = Width
        self.Height = Height
        self.Square = Square
        self.GameBoard = self.Width // 2
        self.Win = Win
        self.Rows = Rows
        self.Cols = Cols
        self.Board = []
        self.create_Board()
        self.promotion_choice = None  # Nueva variable para guardar la opción de promoción

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
        piece.first_move = False  # Marcar que la pieza ha sido movida

        # Verificar si es un peón que llegó al final del tablero
        if piece.type == "Pawn":
            if (piece.color == White and row == 0) or (piece.color == Black and row == 7):
                self.promotion_choice = piece  # Guardar el peón que debe ser promovido



    def draw_Board(self):
        self.Win.fill(CustomBrown)

        font = pygame.font.SysFont(None, 24)
        
        for row in range(self.Rows):
            for col in range(self.Cols):
                color = CustomBeige if (row + col) % 2 == 0 else CustomBrown
                pygame.draw.rect(self.Win, color, (col * self.Square, row * self.Square, self.Square, self.Square))

                # Dibujar los números en las filas
                if col == 0:
                    text = font.render(str(8 - row), True, pygame.Color('gray51'))
                    self.Win.blit(text, (col * self.Square + 5, row * self.Square + 5))

                # Dibujar las letras en las columnas
                if row == 7:
                    text = font.render(chr(97 + col), True, pygame.Color('gray51'))
                    self.Win.blit(text, ((col + 1) * self.Square - 20, (row + 1) * self.Square - 20))

    def draw_piece(self, piece, Win):
        Win.blit(piece.image, (piece.x, piece.y))


    def draw_pieces(self):
        for row in range(self.Rows):
            for col in range(self.Cols):
                if self.Board[row][col] != 0:
                    self.draw_piece(self.Board[row][col], self.Win)

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

            self.promotion_choice = None  # Reiniciar la opción de promoción
