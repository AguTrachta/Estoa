import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from chess_game.Pieces import Pawn
from chess_game.constants import White, Black

#Prueba los movimientos del Peon
class TestPawnMovement(unittest.TestCase):
    def setUp(self):
        self.square = 80  # Tamaño arbitrario del cuadrado
        self.board = [[0] * 8 for _ in range(8)]  # Tablero vacío

    def test_pawn_initial_move(self):
        white_pawn = Pawn(self.square, None, White, "Pawn", 6, 0)
        self.board[6][0] = white_pawn
        moves = white_pawn.get_available_moves(self.board)
        self.assertIn((5, 0), moves)
        self.assertIn((4, 0), moves)

    def test_pawn_capture(self):
        white_pawn = Pawn(self.square, None, White, "Pawn", 6, 0)
        self.board[6][0] = white_pawn
        self.board[5][1] = Pawn(self.square, None, Black, "Pawn", 5, 1)
        moves = white_pawn.get_available_moves(self.board)
        self.assertIn((5, 1), moves)

if __name__ == '__main__':
    unittest.main()