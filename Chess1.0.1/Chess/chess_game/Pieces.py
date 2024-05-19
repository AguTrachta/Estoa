import pygame
from .constants import *

class Piece:
    def __init__(self, Square, image, color, type, row, col):
        self.Square = Square
        self.image = image
        self.color = color
        self.row = row
        self.col = col
        self.type = type
        self.x = 0
        self.y = 0
        self.image = image
        self.available_moves = []
        self.capture_moves = []  # Lista adicional para movimientos de captura
        self.calc_pos()

    def piece_move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * self.Square
        self.y = self.row * self.Square

    def clear_available_moves(self):
        if len(self.available_moves) > 0:
            self.available_moves = []
        if len(self.capture_moves) > 0:
            self.capture_moves = []

class Pawn(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)
        self.first_move = True

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()

        # Trabaja para peones blancos
        if self.color == White:
            if row - 1 >= 0:
                if Board[row - 1][col] == 0:
                    self.available_moves.append((row - 1, col))

                if self.first_move and row - 2 >= 0 and Board[row - 2][col] == 0:
                    self.available_moves.append((row - 2, col))

                if col - 1 >= 0 and Board[row - 1][col - 1] != 0:
                    piece = Board[row - 1][col - 1]
                    if piece.color != self.color:
                        self.capture_moves.append((row - 1, col - 1))

                if col + 1 < len(Board[0]) and Board[row - 1][col + 1] != 0:
                    piece = Board[row - 1][col + 1]
                    if piece.color != self.color:
                        self.capture_moves.append((row - 1, col + 1))

        # Trabaja para peones negros
        if self.color == Black:
            if row + 1 < len(Board):
                if Board[row + 1][col] == 0:
                    self.available_moves.append((row + 1, col))

                if self.first_move and row + 2 < len(Board) and Board[row + 2][col] == 0:
                    self.available_moves.append((row + 2, col))

                if col - 1 >= 0 and row + 1 < len(Board) and Board[row + 1][col - 1] != 0:
                    piece = Board[row + 1][col - 1]
                    if piece.color != self.color:
                        self.capture_moves.append((row + 1, col - 1))

                if col + 1 < len(Board[0]) and row + 1 < len(Board) and Board[row + 1][col + 1] != 0:
                    piece = Board[row + 1][col + 1]
                    if piece.color != self.color:
                        self.capture_moves.append((row + 1, col + 1))

        return self.available_moves + self.capture_moves


class Rook(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()
        for i in range(row + 1, 8):
            if Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board[i][col].color != self.color:
                    self.capture_moves.append((i, col))
                break

        for i in range(row - 1, -1, -1):
            if Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board[i][col].color != self.color:
                    self.capture_moves.append((i, col))
                break

        for i in range(col + 1, 8):
            if Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board[row][i].color != self.color:
                    self.capture_moves.append((row, i))
                break

        for i in range(col - 1, -1, -1):
            if Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board[row][i].color != self.color:
                    self.capture_moves.append((row, i))
                break

        return self.available_moves + self.capture_moves

class Bishop(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()

        # Diagonal abajo-derecha
        row_i, col_i = row + 1, col + 1
        while row_i < 8 and col_i < 8:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i += 1

        # Diagonal arriba-izquierda
        row_i, col_i = row - 1, col - 1
        while row_i >= 0 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i -= 1

        # Diagonal arriba-derecha
        row_i, col_i = row - 1, col + 1
        while row_i >= 0 and col_i < 8:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i += 1

        # Diagonal abajo-izquierda
        row_i, col_i = row + 1, col - 1
        while row_i < 8 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i -= 1

        return self.available_moves + self.capture_moves

class Knight(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()
        directions = [
            (row - 2, col + 1), (row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1),
            (row + 2, col - 1), (row + 1, col - 2), (row - 1, col - 2), (row - 2, col - 1)
        ]

        for move in directions:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:
                if Board[r][c] == 0:
                    self.available_moves.append((r, c))
                elif Board[r][c].color != self.color:
                    self.capture_moves.append((r, c))

        return self.available_moves + self.capture_moves

class Queen(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()

        # Movimientos como la torre
        for i in range(row + 1, 8):
            if Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board[i][col].color != self.color:
                    self.capture_moves.append((i, col))
                break

        for i in range(row - 1, -1, -1):
            if Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board[i][col].color != self.color:
                    self.capture_moves.append((i, col))
                break

        for i in range(col + 1, 8):
            if Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board[row][i].color != self.color:
                    self.capture_moves.append((row, i))
                break

        for i in range(col - 1, -1, -1):
            if Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board[row][i].color != self.color:
                    self.capture_moves.append((row, i))
                break

        # Movimientos como el alfil
        # Diagonal abajo-derecha
        row_i, col_i = row + 1, col + 1
        while row_i < 8 and col_i < 8:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i += 1

        # Diagonal arriba-izquierda
        row_i, col_i = row - 1, col - 1
        while row_i >= 0 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i -= 1

        # Diagonal arriba-derecha
        row_i, col_i = row - 1, col + 1
        while row_i >= 0 and col_i < 8:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i += 1

        # Diagonal abajo-izquierda
        row_i, col_i = row + 1, col - 1
        while row_i < 8 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != self.color:
                    self.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i -= 1

        return self.available_moves + self.capture_moves

class King(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()
        directions = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
        ]

        for move in directions:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:
                if Board[r][c] == 0:
                    self.available_moves.append((r, c))
                elif Board[r][c].color != self.color:
                    self.capture_moves.append((r, c))

        return self.available_moves + self.capture_moves
