from .board import Board
from .view import GameView
from .constants import *

class GameController:
    def __init__(self, width, height, rows, cols, square, win):
        self.board = Board(width, height, rows, cols, square)
        self.view = GameView(win)
        self.selected = None
        self.turn = White
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.in_menu = True
        self.white_time = 300  # 5 minutos en segundos
        self.black_time = 300  # 5 minutos en segundos
        self.last_time = pygame.time.get_ticks()

    def update(self):
        if self.in_menu:
            play_rect, quit_rect = self.view.draw_main_menu()
            return play_rect, quit_rect
        else:
            self.update_timers()
            self.view.draw_board(self.board)
            self.view.draw_pieces(self.board)
            self.view.draw_available_moves(self.selected, self.valid_moves, self.board.Square)
            self.view.draw_timers(self.white_time, self.black_time)
            if self.board.promotion_choice:
                self.view.show_promotion_choices()
            if self.game_over:
                self.view.show_winner(self.winner)
            pygame.display.update()
            return None, None

    def reset(self):
        self.board = Board(self.board.Width, self.board.Height, self.board.Rows, self.board.Cols, self.board.Square)
        self.selected = None
        self.game_over = False
        self.winner = None
        self.turn = White
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.white_time = 300
        self.black_time = 300
        self.last_time = pygame.time.get_ticks()

    def check_game(self):
        if self.Black_pieces_left == 0:
            self.game_over = True
            self.winner = "Whites win"
            return True

        if self.White_pieces_left == 0:
            self.game_over = True
            self.winner = "Blacks win"
            return True

        if self.checkmate(self.board):
            self.game_over = True
            self.winner = "Black Wins" if self.turn == White else "White wins"
            return True
        return False

    def enemies_moves(self, piece, Board):
        enemies_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0 and Board[r][c].color != piece.color:
                    moves = Board[r][c].get_available_moves(Board)
                    for move in moves:
                        enemies_moves.append(move)
        return enemies_moves

    def get_King_pos(self, Board):
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0 and Board[r][c].type == "King" and Board[r][c].color == self.turn:
                    return (r, c)
        return None

    def simulate_move(self, piece, row, col):
        piece_row, piece_col = piece.row, piece.col
        target_piece = self.board.Board[row][col]

        self.board.Board[row][col] = piece
        self.board.Board[piece_row][piece_col] = 0

        piece.row, piece.col = row, col

        king_pos = self.get_King_pos(self.board.Board)
        if king_pos:
            enemy_moves = self.enemies_moves(piece, self.board.Board)
            if king_pos in enemy_moves:
                piece.row, piece.col = piece_row, piece_col
                self.board.Board[row][col] = target_piece
                self.board.Board[piece_row][piece_col] = piece
                return False

        piece.row, piece.col = piece_row, piece_col
        self.board.Board[row][col] = target_piece
        self.board.Board[piece_row][piece_col] = piece
        return True

    def possible_moves(self, board):
        possible_moves = []
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] != 0 and board[r][c].color == self.turn and board[r][c].type != "King":
                    moves = board[r][c].get_available_moves(board)
                    for move in moves:
                        possible_moves.append((r, c, move[0], move[1]))
        return possible_moves

    def checkmate(self, board):
        king_pos = self.get_King_pos(board.Board)
        if not king_pos:
            return False

        king_piece = board.get_piece(king_pos[0], king_pos[1])
        king_available_moves = set(king_piece.get_available_moves(board.Board))
        enemies_moves_set = set(self.enemies_moves(king_piece, board.Board))

        king_moves = set()
        for move in king_available_moves:
            temp_board = self.copy_board(board.Board)
            temp_board[king_piece.row][king_piece.col] = 0
            temp_board[move[0]][move[1]] = king_piece
            if move not in self.enemies_moves(king_piece, temp_board):
                king_moves.add(move)

        if len(king_moves) > 0:
            return False

        all_possible_moves = self.possible_moves(board.Board)
        for move in all_possible_moves:
            r, c, move_r, move_c = move
            piece = board.get_piece(r, c)
            if self.simulate_move(piece, move_r, move_c):
                return False

        return True

    def copy_board(self, board):
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
        self.update_timers()
        if self.turn == White:
            self.turn = Black
        else:
            self.turn = White
        self.last_time = pygame.time.get_ticks()

    def select(self, row, col):
        if self.selected:
            move = self._move(row, col)
            if not move:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and self.turn == piece.color:
            self.selected = piece
            self.valid_moves = piece.get_available_moves(self.board.Board)

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
                if self.selected.type == "King" and abs(self.selected.col - col) == 2:
                    # Enroque
                    self.perform_castling(self.selected, row, col)
                else:
                    if self.simulate_move(self.selected, row, col):
                        self.remove_piece(self.board.Board, piece, row, col)
                        self.board.move(self.selected, row, col)
                        self.change_turn()
                        self.valid_moves = []
                        self.selected = None
                        if self.check_game():  # Verificar el estado del juego después de cada movimiento
                            print(f"Game Over: {self.winner}")
                        return True
        return False

    def perform_castling(self, king, row, col):
        if col == 6:  # Enroque corto
            rook = self.board.get_piece(row, 7)
            self.board.move(king, row, col)
            self.board.move(rook, row, col - 1)
        elif col == 2:  # Enroque largo
            rook = self.board.get_piece(row, 0)
            self.board.move(king, row, col)
            self.board.move(rook, row, col + 1)
        self.change_turn()
        self.valid_moves = []
        self.selected = None
        self.update()  # Actualiza la ventana inmediatamente después del enroque

    def remove_piece(self, board, piece, row, col):
        if piece != 0:
            board[row][col] = 0
            if piece.color == White:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1
        print("White_pieces_left : ", self.White_pieces_left)
        print("Black_pieces_left : ", self.Black_pieces_left)

    def handle_promotion(self, choice):
        if self.board.promotion_choice:
            self.board.promote_pawn(choice)
            self.board.promotion_choice = None  # Reiniciar la opción de promoción

    def handle_menu_click(self, mouse_pos):
        play_rect, quit_rect = self.update()
        if play_rect and play_rect.collidepoint(mouse_pos):
            self.in_menu = False
        elif quit_rect and quit_rect.collidepoint(mouse_pos):
            pygame.quit()
            quit()

    def update_timers(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time) / 1000
        if self.turn == White:
            self.white_time -= elapsed_time
        else:
            self.black_time -= elapsed_time
        self.last_time = current_time
        if self.white_time <= 0:
            self.game_over = True
            self.winner = "Black Wins by Timeout"
        elif self.black_time <= 0:
            self.game_over = True
            self.winner = "White Wins by Timeout"
