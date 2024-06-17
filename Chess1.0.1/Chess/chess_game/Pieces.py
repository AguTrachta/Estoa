import pygame
from .constants import *
from abc import ABC, abstractmethod

class Piece:
    def __init__(self, Square, image, color, type, row, col, move_strategy):
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
        self.capture_moves = []
        self.calc_pos()
        self.move_strategy = move_strategy

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
            
    def get_available_moves(self, Board):
        return self.move_strategy.get_available_moves(self, Board)

class MoveStrategy(ABC):
    @abstractmethod
    def get_available_moves(self, piece, Board):
        pass

class PawnMoveStrategy(MoveStrategy):
    def get_available_moves(self, piece, Board):
        piece.clear_available_moves()
        row, col = piece.row, piece.col

        if piece.color == White:
            if row - 1 >= 0:
                if Board[row - 1][col] == 0:
                    piece.available_moves.append((row - 1, col))
                    if piece.first_move and row - 2 >= 0 and Board[row - 2][col] == 0:
                        piece.available_moves.append((row - 2, col))
                if col - 1 >= 0 and Board[row - 1][col - 1] != 0 and Board[row - 1][col - 1].color != piece.color:
                    piece.capture_moves.append((row - 1, col - 1))
                if col + 1 < len(Board[0]) and Board[row - 1][col + 1] != 0 and Board[row - 1][col + 1].color != piece.color:
                    piece.capture_moves.append((row - 1, col + 1))

        if piece.color == Black:
            if row + 1 < len(Board):
                if Board[row + 1][col] == 0:
                    piece.available_moves.append((row + 1, col))
                    if piece.first_move and row + 2 < len(Board) and Board[row + 2][col] == 0:
                        piece.available_moves.append((row + 2, col))
                if col - 1 >= 0 and Board[row + 1][col - 1] != 0 and Board[row + 1][col - 1].color != piece.color:
                    piece.capture_moves.append((row + 1, col - 1))
                if col + 1 < len(Board[0]) and Board[row + 1][col + 1] != 0 and Board[row + 1][col + 1].color != piece.color:
                    piece.capture_moves.append((row + 1, col + 1))

        return piece.available_moves + piece.capture_moves


class RookMoveStrategy(MoveStrategy):
    def get_available_moves(self, piece, Board):
        piece.clear_available_moves()
        row, col = piece.row, piece.col

        for i in range(row + 1, len(Board)):
            if Board[i][col] == 0:
                piece.available_moves.append((i, col))
            else:
                if Board[i][col].color != piece.color:
                    piece.capture_moves.append((i, col))
                break

        for i in range(row - 1, -1, -1):
            if Board[i][col] == 0:
                piece.available_moves.append((i, col))
            else:
                if Board[i][col].color != piece.color:
                    piece.capture_moves.append((i, col))
                break

        for i in range(col + 1, len(Board[0])):
            if Board[row][i] == 0:
                piece.available_moves.append((row, i))
            else:
                if Board[row][i].color != piece.color:
                    piece.capture_moves.append((row, i))
                break

        for i in range(col - 1, -1, -1):
            if Board[row][i] == 0:
                piece.available_moves.append((row, i))
            else:
                if Board[row][i].color != piece.color:
                    piece.capture_moves.append((row, i))
                break

        return piece.available_moves + piece.capture_moves



class BishopMoveStrategy(MoveStrategy):
    def get_available_moves(self, piece, Board):
        piece.clear_available_moves()
        row, col = piece.row, piece.col

        # Diagonal abajo-derecha
        row_i, col_i = row + 1, col + 1
        while row_i < len(Board) and col_i < len(Board[0]):
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i += 1

        # Diagonal arriba-izquierda
        row_i, col_i = row - 1, col - 1
        while row_i >= 0 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i -= 1

        # Diagonal arriba-derecha
        row_i, col_i = row - 1, col + 1
        while row_i >= 0 and col_i < len(Board[0]):
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i += 1

        # Diagonal abajo-izquierda
        row_i, col_i = row + 1, col - 1
        while row_i < len(Board) and col_i >= 0:
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i -= 1

        return piece.available_moves + piece.capture_moves

class KnightMoveStrategy(MoveStrategy):
    def get_available_moves(self, piece, Board):
        piece.clear_available_moves()
        row, col = piece.row, piece.col
        moves = [
            (row - 2, col - 1), (row - 2, col + 1), (row - 1, col - 2), (row - 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1), (row + 1, col - 2), (row + 1, col + 2)
        ]

        #print(f"Calculating moves for Knight at ({row}, {col})")

        for move in moves:
            r, c = move
            if 0 <= r < len(Board) and 0 <= c < len(Board[0]):
                if Board[r][c] == 0:
                    piece.available_moves.append((r, c))
                elif Board[r][c].color != piece.color:
                    piece.capture_moves.append((r, c))

        #print(f"Available moves: {piece.available_moves}")
        #print(f"Capture moves: {piece.capture_moves}")

        return piece.available_moves + piece.capture_moves


class QueenMoveStrategy(MoveStrategy):
    def get_available_moves(self, piece, Board):
        piece.clear_available_moves()
        row, col = piece.row, piece.col

        # Movimientos como la torre
        for i in range(row + 1, 8):
            if Board[i][col] == 0:
                piece.available_moves.append((i, col))
            else:
                if Board[i][col].color != piece.color:
                    piece.capture_moves.append((i, col))
                break

        for i in range(row - 1, -1, -1):
            if Board[i][col] == 0:
                piece.available_moves.append((i, col))
            else:
                if Board[i][col].color != piece.color:
                    piece.capture_moves.append((i, col))
                break

        for i in range(col + 1, 8):
            if Board[row][i] == 0:
                piece.available_moves.append((row, i))
            else:
                if Board[row][i].color != piece.color:
                    piece.capture_moves.append((row, i))
                break

        for i in range(col - 1, -1, -1):
            if Board[row][i] == 0:
                piece.available_moves.append((row, i))
            else:
                if Board[row][i].color != piece.color:
                    piece.capture_moves.append((row, i))
                break

        # Movimientos como el alfil
        row_i, col_i = row + 1, col + 1
        while row_i < 8 and col_i < 8:
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i += 1

        row_i, col_i = row - 1, col - 1
        while row_i >= 0 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i -= 1

        row_i, col_i = row - 1, col + 1
        while row_i >= 0 and col_i < 8:
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i -= 1
            col_i += 1

        row_i, col_i = row + 1, col - 1
        while row_i < 8 and col_i >= 0:
            if Board[row_i][col_i] == 0:
                piece.available_moves.append((row_i, col_i))
            else:
                if Board[row_i][col_i].color != piece.color:
                    piece.capture_moves.append((row_i, col_i))
                break
            row_i += 1
            col_i -= 1

        return piece.available_moves + piece.capture_moves

class KingMoveStrategy(MoveStrategy):
    def get_available_moves(self, piece, Board):
        piece.clear_available_moves()
        row, col = piece.row, piece.col
        directions = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
        ]

        for move in directions:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:
                if Board[r][c] == 0:
                    piece.available_moves.append((r, c))
                elif Board[r][c].color != piece.color:
                    piece.capture_moves.append((r, c))

        # Verificar enroque
        if piece.first_move and not self.is_in_check(piece, Board):
            # Enroque corto
            if col + 3 < 8 and isinstance(Board[row][col + 3], Rook) and Board[row][col + 3].first_move:
                if all(Board[row][col + i] == 0 for i in range(1, 3)):
                    if not self.is_in_check_path(piece, Board, [(row, col + 1), (row, col + 2)]):
                        piece.available_moves.append((row, col + 2))  # Enroque corto

            # Enroque largo
            if col - 4 >= 0 and isinstance(Board[row][col - 4], Rook) and Board[row][col - 4].first_move:
                if all(Board[row][col - i] == 0 for i in range(1, 4)):
                    if not self.is_in_check_path(piece, Board, [(row, col - 1), (row, col - 2)]):
                        piece.available_moves.append((row, col - 2))  # Enroque largo

        return piece.available_moves + piece.capture_moves

    def is_in_check(self, piece, Board):
        king_pos = (piece.row, piece.col)
        enemies_moves = set(self.enemies_moves(piece, Board))
        return king_pos in enemies_moves

    def is_in_check_path(self, piece, Board, path):
        enemies_moves = set(self.enemies_moves(piece, Board))
        return any(pos in enemies_moves for pos in path)
    
    def enemies_moves(self, piece, Board):
        enemies_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0 and Board[r][c].color != piece.color and Board[r][c].type != "King":
                    moves = Board[r][c].move_strategy.get_available_moves(Board[r][c], Board)
                    for move in moves:
                        enemies_moves.append(move)
        return enemies_moves

class Pawn(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col, PawnMoveStrategy())
        self.first_move = True

class Rook(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col, RookMoveStrategy())
        self.first_move = True

class Bishop(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col, BishopMoveStrategy())

class Knight(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col, KnightMoveStrategy())

class Queen(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col, QueenMoveStrategy())

class King(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col, KingMoveStrategy())
        self.first_move = True