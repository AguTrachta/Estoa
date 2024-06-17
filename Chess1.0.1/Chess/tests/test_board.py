import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from chess_game.board import Board
from chess_game.constants import White, Black
from chess_game.Pieces import Pawn, Rook

# Verificar que el tablero se inicialice correctamente con las piezas en las posiciones correctas.
class TestBoardInitialization(unittest.TestCase):
    def setUp(self):
        self.width = 800
        self.height = 800
        self.rows = 8
        self.cols = 8
        self.square = self.width // self.cols
        self.board = Board(self.width, self.height, self.rows, self.cols, self.square)

    def test_board_initialization(self):
        self.board.create_Board()
        self.assertIsInstance(self.board.Board[1][0], Pawn)
        self.assertIsInstance(self.board.Board[6][0], Pawn)
        self.assertIsInstance(self.board.Board[0][0], Rook)
        self.assertIsInstance(self.board.Board[7][0], Rook)

if __name__ == '__main__':
    unittest.main()
