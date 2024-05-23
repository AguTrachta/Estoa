# game.py

import pygame
from .board import newBoard
from .constants import *
from copy import deepcopy


class Game:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Width = Width
        self.Height = Height
        self.Win = Win
        self.Board = newBoard(Width, Height, Rows, Cols, Square, Win)
        self.Square = Square
        self.selected = None
        self.turn = White
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.game_over = False
        self.winner = None

    def update_window(self):
        self.Board.draw_Board()
        self.Board.draw_pieces()
        self.draw_available_moves()
        if self.Board.promotion_choice:
            self.show_promotion_choices()
        if self.game_over:
            self.show_winner()
        pygame.display.update()

    def reset(self):
        self.Board = newBoard(self.Width, self.Height, self.Rows, self.Cols, self.Square, self.Win)
        self.Square = self.Square
        self.selected = None
        self.game_over = False
        self.winner = None
        self.turn = White
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        print("Game reset")

    def check_game(self):
        if self.Black_pieces_left == 0:
            self.game_over = True
            self.winner = "Whites win"
            print("Game Over: Whites win")
            return True

        if self.White_pieces_left == 0:
            self.game_over = True
            self.winner = "Blacks win"
            print("Game Over: Blacks win")
            return True

        if self.checkmate(self.Board):
            self.game_over = True
            if self.turn == White:
                self.winner = "Black Wins"
            else:
                self.winner = "White wins"
            print(f"Game Over: {self.winner}")
            return True
        return False

    def enemies_moves(self, piece, Board):
        enemies_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color != piece.color:
                        moves = Board[r][c].get_available_moves(r, c, Board)
                        for move in moves:
                            enemies_moves.append(move)
        return enemies_moves

    def get_King_pos(self, Board):
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].type == "King" and Board[r][c].color == self.turn:
                        return (r, c)
        return None

    def simulate_move(self, piece, row, col):
        piece_row, piece_col = piece.row, piece.col
        target_piece = self.Board.Board[row][col]

        # Realizar el movimiento en el tablero temporalmente
        self.Board.Board[row][col] = piece
        self.Board.Board[piece_row][piece_col] = 0

        # Actualizar la posición de la pieza
        piece.row, piece.col = row, col

        # Verificar si el rey está en jaque después del movimiento
        king_pos = self.get_King_pos(self.Board.Board)
        if king_pos:
            enemy_moves = self.enemies_moves(piece, self.Board.Board)
            if king_pos in enemy_moves:
                # Restaurar el estado del tablero si el movimiento pone al rey en jaque
                piece.row, piece.col = piece_row, piece_col
                self.Board.Board[row][col] = target_piece
                self.Board.Board[piece_row][piece_col] = piece
                return False

        # Restaurar la posición original de la pieza y el estado del tablero
        piece.row, piece.col = piece_row, piece_col
        self.Board.Board[row][col] = target_piece
        self.Board.Board[piece_row][piece_col] = piece
        return True

    def possible_moves(self, Board):
        possible_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color == self.turn and Board[r][c].type != "King":
                        moves = Board[r][c].get_available_moves(r, c, Board)
                        for move in moves:
                            possible_moves.append((r, c, move[0], move[1]))  # Include piece position and move position
        return possible_moves

    def checkmate(self, Board):
        king_pos = self.get_King_pos(Board.Board)
        if not king_pos:
            print("No king found")
            return False

        print(f"King position: {king_pos}")
        get_king = Board.get_piece(king_pos[0], king_pos[1])
        king_available_moves = set(get_king.get_available_moves(king_pos[0], king_pos[1], Board.Board))
        enemies_moves_set = set(self.enemies_moves(get_king, Board.Board))

        # Verificar si algún movimiento del rey lo pone fuera de peligro
        king_moves = set()
        for move in king_available_moves:
            temp_board = self.copy_board(Board.Board)
            temp_board[get_king.row][get_king.col] = 0
            temp_board[move[0]][move[1]] = get_king
            if move not in self.enemies_moves(get_king, temp_board):
                king_moves.add(move)

        if len(king_moves) > 0:
            print(f"King has safe moves: {king_moves}")
            return False

        # Verificar si alguna pieza puede bloquear el jaque o capturar la pieza atacante
        all_possible_moves = self.possible_moves(Board.Board)
        for move in all_possible_moves:
            r, c, move_r, move_c = move
            piece = Board.get_piece(r, c)
            if self.simulate_move(piece, move_r, move_c):
                print(f"Move {move} can block the check")
                return False

        print(f"Checkmate detected for {'White' if self.turn == Black else 'Black'}")
        return True

    def copy_board(self, board):
        # Crear una copia manual del tablero sin superficies de Pygame
        new_board = []
        for row in board:
            new_row = []
            for piece in row:
                if piece == 0:
                    new_row.append(0)
                else:
                    new_row.append(
                        piece.__class__(piece.Square, piece.image, piece.color, piece.type, piece.row, piece.col))
            new_board.append(new_row)
        return new_board

    def change_turn(self):
        if self.turn == White:
            self.turn = Black
        else:
            self.turn = White

    def select(self, row, col):
        if self.selected:
            move = self._move(row, col)
            if not move:
                self.selected = None
                self.select(row, col)

        piece = self.Board.get_piece(row, col)
        if piece != 0 and self.turn == piece.color:
            self.selected = piece
            self.valid_moves = piece.get_available_moves(row, col, self.Board.Board)

    def _move(self, row, col):
        piece = self.Board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
                if self.simulate_move(self.selected, row, col):
                    self.remove(self.Board.Board, piece, row, col)
                    self.Board.move(self.selected, row, col)
                    self.change_turn()
                    self.valid_moves = []
                    self.selected = None
                    return True
                return False
        return False

    def remove(self, board, piece, row, col):
        if piece != 0:
            board[row][col] = 0
            if piece.color == White:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1
        print("White_pieces_left : ", self.White_pieces_left)
        print("Black_pieces_left : ", self.Black_pieces_left)

    def draw_available_moves(self):
        if self.selected is not None:
            if len(self.selected.available_moves) > 0 or len(self.selected.capture_moves) > 0:
                for pos in self.selected.available_moves:
                    row, col = pos[0], pos[1]
                    pygame.draw.circle(self.Win, Green,
                                       (col * self.Square + self.Square // 2, row * self.Square + self.Square // 2),
                                       self.Square // 8)
                for pos in self.selected.capture_moves:
                    row, col = pos[0], pos[1]
                    pygame.draw.circle(self.Win, Red,
                                       (col * self.Square + self.Square // 2, row * self.Square + self.Square // 2),
                                       self.Square // 8)

    def get_board(self):
        return self.board

    def show_winner(self):
        # Crear una superficie semi-transparente para el fondo del mensaje
        overlay = pygame.Surface((self.Width, self.Height))
        overlay.set_alpha(180)  # Transparencia: 0 (completamente transparente) a 255 (completamente opaco)
        overlay.fill((0, 0, 0))  # Color del fondo (negro)
        self.Win.blit(overlay, (0, 0))

        # Configurar la fuente y el tamaño del texto
        font = pygame.font.SysFont('Arial', 72, bold=True)
        text = font.render(self.winner, True, (255, 255, 255))  # Texto en blanco

        # Obtener las dimensiones del texto para centrarlo en la pantalla
        text_rect = text.get_rect(center=(self.Width // 2, self.Height // 2))

        # Dibujar el texto en la ventana
        self.Win.blit(text, text_rect)
        pygame.display.update()
        print(f"Winner displayed: {self.winner}")

    # game.py

    def show_promotion_choices(self):
        # Crear una superficie semi-transparente para el fondo del mensaje
        overlay = pygame.Surface((self.Width, self.Height))
        overlay.set_alpha(180)  # Transparencia: 0 (completamente transparente) a 255 (completamente opaco)
        overlay.fill((0, 0, 0))  # Color del fondo (negro)
        self.Win.blit(overlay, (0, 0))

        # Configurar la fuente y el tamaño del texto
        font = pygame.font.SysFont('Arial', 36, bold=True)
        choices = ["Queen", "Rook", "Bishop", "Knight"]
        choice_texts = [font.render(choice, True, (255, 255, 255)) for choice in choices]

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Dibujar las opciones en la ventana con efecto de hover
        for i, text in enumerate(choice_texts):
            text_rect = text.get_rect(center=(self.Width // 2, self.Height // 2 - 75 + i * 50))

            # Verificar si el mouse está sobre la opción
            if text_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.Win, (150, 150, 150),
                                 text_rect.inflate(20, 10))  # Color de fondo para el efecto de hover

            self.Win.blit(text, text_rect)

        pygame.display.update()
        print("Promotion choices displayed")

    def handle_promotion(self, choice):
        if self.Board.promotion_choice:
            self.Board.promote_pawn(choice)
            self.Board.promotion_choice = None