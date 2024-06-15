
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chess_game.game import Game
from chess_game.Pieces import King, Rook
from chess_game.constants import White, Black

class TestSimulateMove(unittest.TestCase):
    def setUp(self):
        self.width = 800  # Ancho del tablero
        self.height = 800  # Altura del tablero
        self.rows = 8  # Número de filas
        self.cols = 8  # Número de columnas
        self.square = 80  # Ejemplo de creación de un objeto Square
        self.square_size = self.width // self.cols  # Tamaño de cada cuadrado
        self.win = None  # Placeholder para la ventana (puedes ajustar según tu implementación)

        self.game = Game(self.width, self.height, self.rows, self.cols, self.square_size, self.win)

    def test_simulate_simple_check(self):
        # Crear una configuración simple con solo un rey y una torre enemiga
        king = King(self.square, None, White, "King", 7, 4)
        rook = Rook(self.square, None, Black, "Rook", 5, 4)  # Torre negra en (5, 4)

        # Colocar las piezas en el tablero
        self.game.Board.Board[5][4] = rook
        self.game.Board.Board[0][4] = king
        #se testea simulate_move()
        # Simular mover el rey a una posición que lo pone en jaque (por ejemplo, mover el rey hacia adelante a (1, 4))
        result = self.game.simulate_move(king, 1, 4)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()



