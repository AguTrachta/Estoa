import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock, patch
import pygame
from chess_game.Pieces import King, Rook
from chess_game.constants import White, Black
from chess_game.controller import GameController

class TestCastling(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.font.init()  # Inicializar las fuentes de Pygame
        self.width = 680
        self.height = 680
        self.rows = 8
        self.cols = 8
        self.square = self.width // self.cols
        self.win = Mock()  # Mock para la ventana de pygame
        self.controller = GameController(self.width, self.height, self.rows, self.cols, self.square, self.win)

    def tearDown(self):
        pygame.quit()

    @patch.object(GameController, 'update')
    def test_kingside_castling_white(self, mock_update):
        # Preparar el tablero para enroque corto blanco
        self.controller.board.Board[7][4] = King(self.square, None, White, "King", 7, 4)
        self.controller.board.Board[7][7] = Rook(self.square, None, White, "Rook", 7, 7)
        self.controller.board.Board[7][5] = 0
        self.controller.board.Board[7][6] = 0

        # Realizar el enroque corto
        self.controller.selected = self.controller.board.Board[7][4]
        self.controller.valid_moves = [(7, 6)]
        self.controller._move(7, 6)

        # Verificar las posiciones del rey y la torre después del enroque corto
        self.assertIsInstance(self.controller.board.get_piece(7, 6), King)
        self.assertIsInstance(self.controller.board.get_piece(7, 5), Rook)

    @patch.object(GameController, 'update')
    def test_queenside_castling_white(self, mock_update):
        # Preparar el tablero para enroque largo blanco
        self.controller.board.Board[7][4] = King(self.square, None, White, "King", 7, 4)
        self.controller.board.Board[7][0] = Rook(self.square, None, White, "Rook", 7, 0)
        self.controller.board.Board[7][1] = 0
        self.controller.board.Board[7][2] = 0
        self.controller.board.Board[7][3] = 0

        # Realizar el enroque largo
        self.controller.selected = self.controller.board.Board[7][4]
        self.controller.valid_moves = [(7, 2)]
        self.controller._move(7, 2)

        # Verificar las posiciones del rey y la torre después del enroque largo
        self.assertIsInstance(self.controller.board.get_piece(7, 2), King)
        self.assertIsInstance(self.controller.board.get_piece(7, 3), Rook)

    @patch.object(GameController, 'update')
    def test_kingside_castling_black(self, mock_update):
        # Preparar el tablero para enroque corto negro
        self.controller.board.Board[0][4] = King(self.square, None, Black, "King", 0, 4)
        self.controller.board.Board[0][7] = Rook(self.square, None, Black, "Rook", 0, 7)
        self.controller.board.Board[0][5] = 0
        self.controller.board.Board[0][6] = 0

        # Realizar el enroque corto
        self.controller.selected = self.controller.board.Board[0][4]
        self.controller.valid_moves = [(0, 6)]
        self.controller._move(0, 6)

        # Verificar las posiciones del rey y la torre después del enroque corto
        self.assertIsInstance(self.controller.board.get_piece(0, 6), King)
        self.assertIsInstance(self.controller.board.get_piece(0, 5), Rook)

    @patch.object(GameController, 'update')
    def test_queenside_castling_black(self, mock_update):
        # Preparar el tablero para enroque largo negro
        self.controller.board.Board[0][4] = King(self.square, None, Black, "King", 0, 4)
        self.controller.board.Board[0][0] = Rook(self.square, None, Black, "Rook", 0, 0)
        self.controller.board.Board[0][1] = 0
        self.controller.board.Board[0][2] = 0
        self.controller.board.Board[0][3] = 0

        # Realizar el enroque largo
        self.controller.selected = self.controller.board.Board[0][4]
        self.controller.valid_moves = [(0, 2)]
        self.controller._move(0, 2)

        # Verificar las posiciones del rey y la torre después del enroque largo
        self.assertIsInstance(self.controller.board.get_piece(0, 2), King)
        self.assertIsInstance(self.controller.board.get_piece(0, 3), Rook)

if __name__ == "__main__":
    unittest.main()
