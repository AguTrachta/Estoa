import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
import pygame
from chess_game.Pieces import King, Queen, Rook
from chess_game.constants import White, Black
from chess_game.controller import GameController
from chess_game.board import Board

class TestCheckmate(unittest.TestCase):
    def setUp(self):
        # Inicializar el juego
        pygame.init()
        self.Width = 800
        self.Height = 800
        self.Rows = 8
        self.Cols = 8
        self.Square = self.Width // self.Cols
        self.Win = Mock()  # Mock para la ventana de pygame
        self.controller = GameController(self.Width, self.Height, self.Rows, self.Cols, self.Square, self.Win)

        # Crear un tablero vacío
        self.controller.board.Board = [[0] * self.Cols for _ in range(self.Rows)]

        # Crear una superficie vacía para las imágenes de las piezas
        self.empty_surface = pygame.Surface((self.Square, self.Square))

    def test_checkmate(self):
        # Colocar las piezas en una situación de jaque mate
        # Rey negro en (7, 4)
        # Reina blanca en (6, 2)
        # Torre blanca en (7, 0)
        black_king = King(self.Square, self.empty_surface, Black, "King", 7, 4)
        white_queen = Queen(self.Square, self.empty_surface, White, "Queen", 6, 2)
        white_rook = Rook(self.Square, self.empty_surface, White, "Rook", 7, 0)

        self.controller.board.Board[7][4] = black_king
        self.controller.board.Board[6][2] = white_queen
        self.controller.board.Board[7][0] = white_rook

        # Cambiar el turno a las negras
        self.controller.turn = Black

        # Comprobar que se detecta el jaque mate
        self.assertTrue(self.controller.check_game())
        self.assertEqual(self.controller.winner, "White wins")
        print(f"Winner: {self.controller.winner}")

        # Verificar que se muestra el mensaje de jaque mate
        self.assertIsNotNone(self.controller.winner)

if __name__ == "__main__":
    unittest.main()
