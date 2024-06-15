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
            self.update_window()
            return True

        if self.White_pieces_left == 0:
            self.game_over = True
            self.winner = "Blacks win"
            print("Game Over: Blacks win")
            self.update_window()
            return True

        if self.is_stalemate(self.Board):  # Verificación de ahogado
            self.game_over = True
            self.winner = "Stalemate - Draw"
            print("Game Over: Stalemate")
            self.update_window()
            return True

        if self.checkmate(self.Board):
            self.game_over = True
            if self.turn == White:
                self.winner = "Black Wins"
            else:
                self.winner = "White wins"
            print(f"Game Over: {self.winner}")
            self.update_window()
            return True

        return False


    def enemies_moves(self, piece, Board):
        enemies_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color != piece.color:
                        moves = Board[r][c].get_available_moves(Board)
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
            #print(f"Posición del rey: {king_pos}")
            enemy_moves = self.enemies_moves(piece, self.Board.Board)
            #print(f"Movimientos enemigos: {enemy_moves}")
            if king_pos in enemy_moves:
                print(f"El rey está en jaque después del movimiento: {piece} a ({row}, {col})")
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
                        moves = Board[r][c].get_available_moves(Board)
                        for move in moves:
                            possible_moves.append((r, c, move[0], move[1]))  # Include piece position and move position
        return possible_moves

    def is_stalemate(self, Board):
        king_pos = self.get_King_pos(Board.Board)
        if not king_pos:
            print("No king found")
            return False

        king_piece = Board.get_piece(king_pos[0], king_pos[1])
        king_available_moves = set(king_piece.get_available_moves(Board.Board))
        enemies_moves_set = set(self.enemies_moves(king_piece, Board.Board))

        # Verificar si el rey está en jaque
        king_in_check = king_pos in enemies_moves_set

        if king_in_check:
            return False  # No es ahogado si el rey está en jaque

        # Verificar si el rey tiene movimientos legales
        king_safe_moves = set()
        for move in king_available_moves:
            temp_board = self.copy_board(Board.Board)
            temp_board[king_piece.row][king_piece.col] = 0
            temp_board[move[0]][move[1]] = king_piece
            if move not in self.enemies_moves(king_piece, temp_board):
                king_safe_moves.add(move)

        if len(king_safe_moves) > 0:
            print(f"King has safe moves: {king_safe_moves}")
            return False  # No es ahogado si el rey tiene movimientos seguros

        # Verificar si el jugador tiene movimientos legales
        all_possible_moves = self.possible_moves(Board.Board)
        for move in all_possible_moves:
            r, c, move_r, move_c = move
            piece = Board.get_piece(r, c)
            if piece.color == self.turn:
                if self.simulate_move(piece, move_r, move_c):
                    print(f"Move {move} is a legal move")
                    return False  # No es ahogado si alguna pieza tiene movimientos legales

        print("Stalemate detected")
        return True

    def checkmate(self, Board):
        king_pos = self.get_King_pos(Board.Board)
        if not king_pos:
            print("No king found")
            return False

        print(f"King position: {king_pos}")
        king_piece = Board.get_piece(king_pos[0], king_pos[1])
        king_available_moves = set(king_piece.get_available_moves(Board.Board))
        enemies_moves_set = set(self.enemies_moves(king_piece, Board.Board))

        # Verificar si el rey está en jaque
        if king_pos in enemies_moves_set:
            print(f"King is in check at position: {king_pos}")
            king_in_check = True
        else:
            print(f"King is not in check at position: {king_pos}")
            king_in_check = False

        # Verificar si algún movimiento del rey lo pone fuera de peligro
        king_safe_moves = set()
        for move in king_available_moves:
            temp_board = self.copy_board(Board.Board)
            temp_board[king_piece.row][king_piece.col] = 0
            temp_board[move[0]][move[1]] = king_piece
            if move not in self.enemies_moves(king_piece, temp_board):
                king_safe_moves.add(move)

        if len(king_safe_moves) > 0:
            print(f"King has safe moves: {king_safe_moves}")
            return False

        # Verificar si alguna pieza puede bloquear el jaque o capturar la pieza atacante
        all_possible_moves = self.possible_moves(Board.Board)
        for move in all_possible_moves:
            r, c, move_r, move_c = move
            piece = Board.get_piece(r, c)
            if self.simulate_move(piece, move_r, move_c):
                print(f"Move {move} can block the check")
                return False

        if king_in_check:
            print(f"Checkmate detected for {'White' if self.turn == Black else 'Black'}")
            return True
        else:
            print(f"Stalemate detected for {'White' if self.turn == Black else 'Black'}")
            return False


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
            self.valid_moves = piece.get_available_moves(self.Board.Board)

            print(f"Selected {piece.type} at ({row}, {col})")
            print(f"Valid moves: {self.valid_moves}")

    def _move(self, row, col):
        piece = self.Board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
                if self.selected.type == "King" and abs(self.selected.col - col) == 2:
                    # Enroque
                    self.perform_castling(self.selected, row, col)
                else:
                    if self.simulate_move(self.selected, row, col):
                        self.remove(self.Board.Board, piece, row, col)
                        self.Board.move(self.selected, row, col)
                        self.change_turn()
                        self.valid_moves = []
                        self.selected = None
                        return True
        return False

    def perform_castling(self, king, row, col):
        if col == 6:  # Enroque corto
            rook = self.Board.get_piece(row, 7)
            self.Board.move(king, row, col)
            self.Board.move(rook, row, col - 1)
        elif col == 2:  # Enroque largo
            rook = self.Board.get_piece(row, 0)
            self.Board.move(king, row, col)
            self.Board.move(rook, row, col + 1)
        self.change_turn()
        self.valid_moves = []
        self.selected = None

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
            for pos in self.valid_moves:  # Cambiado de self.selected.available_moves a self.valid_moves
                row, col = pos[0], pos[1]
                # Verificar si el movimiento es un enroque
                if self.selected.type == "King" and abs(self.selected.col - col) == 2:
                    color = (0, 0, 255)  # Azul para el enroque
                else:
                    color = (0, 255, 0)  # Verde para otros movimientos

                pygame.draw.circle(self.Win, color,
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
            self.Board.promotion_choice = None  # Reiniciar la opción de promoción
