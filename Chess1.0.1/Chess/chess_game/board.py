import pygame
from chess_game.Pieces import *
from chess_game.constants import *

class newBoard:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.label_space= label_space
        self.Width = Width + 2 * self.label_space
        self.Height = Height + 2 * self.label_space
        self.Square = Square
        self.GameBoard = self.Width // 2
        self.Win = Win
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

    def draw_Board(self):
        self.Win.fill(CustomBrown)

        # Dessiner les cases du plateau
        for row in range(self.Rows):
            for col in range(row % 2, self.Cols, 2):
                pygame.draw.rect(self.Win, CustomBeige, (col * self.Square + self.label_space, row * self.Square + self.label_space, self.Square, self.Square))

        # Création de l'objet de police
        font = pygame.font.SysFont(None, 24)

        # Dessiner les chiffres des lignes (bordures gauche et droite)
        for i in range(self.Rows):
            num = font.render(str(self.Rows - i), True, pygame.Color('black'))
            self.Win.blit(num, (10, i * self.Square + self.label_space + self.Square // 2 - num.get_height() // 2))  # Bord gauche
            self.Win.blit(num, (self.Width - self.label_space + 10, i * self.Square + self.label_space + self.Square // 2 - num.get_height() // 2))  # Bord droit

        # Dessiner les lettres des colonnes (bordures haute et basse)
        for i in range(self.Cols):
            letter = font.render(chr(65 + i), True, pygame.Color('black'))
            self.Win.blit(letter, (i * self.Square + self.label_space + self.Square // 2 - letter.get_width() // 2, self.Height - self.label_space + 10))  # Bord bas
            self.Win.blit(letter, (i * self.Square + self.label_space + self.Square // 2 - letter.get_width() // 2, 10))  # Bord haut

    def draw_piece(self, piece, Win):
        Win.blit(piece.image, (piece.x + self.label_space, piece.y + self.label_space))

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

            self.promotion_choice = None