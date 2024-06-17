import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock
from chess_game.Pieces import King, Rook
from chess_game.constants import White, Black
from chess_game.controller import GameController

class TestSimulateMove(unittest.TestCase):
    def setUp(self):
        self.width = 800  # Ancho del tablero
        self.height = 800  # Altura del tablero
        self.rows = 8  # Número de filas
        self.cols = 8  # Número de columnas
        self.square = 80  # Ejemplo de creación de un objeto Square
        self.square_size = self.width // self.cols  # Tamaño de cada cuadrado
        self.win = Mock()  # Mock para la ventana de pygame

        self.controller = GameController(self.width, self.height, self.rows, self.cols, self.square_size, self.win)

    def test_simulate_simple_check(self):
        # Crear una configuración simple con solo un rey y una torre enemiga
        king = King(self.square, None, White, "King", 7, 4)
        rook = Rook(self.square, None, Black, "Rook", 5, 4)  # Torre negra en (5, 4)

        # Colocar las piezas en el tablero
        self.controller.board.Board[7][4] = king
        self.controller.board.Board[5][4] = rook

        # Simular mover el rey a una posición que lo pone en jaque (por ejemplo, mover el rey hacia adelante a (6, 4))
        result = self.controller.simulate_move(king, 6, 4)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
