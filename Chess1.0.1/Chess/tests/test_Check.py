import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from chess_game.Pieces import King, Queen, Rook
from chess_game.constants import White, Black
from chess_game.controller import GameController
from chess_game.board import Board

class TestCheckmate(unittest.TestCase):
    def setUp(self):
        # Crear el tablero y el juego
        self.width = 800
        self.height = 800
        self.rows = 8
        self.cols = 8
        self.square = self.width // self.cols
        self.win = Mock()  # Mock para la ventana de pygame
        self.board = Board(self.width, self.height, self.rows, self.cols, self.square)
        self.controller = GameController(self.width, self.height, self.rows, self.cols, self.square, self.win)
        
        # Crear un tablero vacío
        self.board.Board = [[0] * self.board.Cols for _ in range(self.board.Rows)]
        self.controller.board = self.board  # Asignar el tablero vacío al controlador

    def test_checkmate(self):
        # Colocar las piezas en una situación de jaque mate
        # Rey negro en (7, 4)
        # Reina blanca en (6, 2)
        # Torre blanca en (7, 0)
        black_king = King(self.square, Mock(), Black, "King", 7, 4)
        white_queen = Queen(self.square, Mock(), White, "Queen", 6, 2)
        white_rook = Rook(self.square, Mock(), White, "Rook", 7, 0)
        
        self.board.Board[7][4] = black_king
        self.board.Board[6][2] = white_queen
        self.board.Board[7][0] = white_rook

        # Cambiar el turno a las negras
        self.controller.turn = Black

        # Comprobar que se detecta el jaque mate
        self.assertTrue(self.controller.check_game())
        self.assertEqual(self.controller.winner, "White wins")

if __name__ == "__main__":
    unittest.main()
