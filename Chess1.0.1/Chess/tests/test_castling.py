import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from chess_game.Pieces import King, Rook
from chess_game.constants import White, Black
from chess_game.game import Game

class TestCastling(unittest.TestCase):
    def setUp(self):
        # Inicializar el juego
        pygame.init()
        self.Width = 800
        self.Height = 800
        self.Rows = 8
        self.Cols = 8
        self.Square = self.Width // self.Cols
        self.Win = pygame.display.set_mode((self.Width, self.Height))  # Crear una ventana real
        self.game = Game(self.Width, self.Height, self.Rows, self.Cols, self.Square, self.Win)

        # Crear un tablero vacío
        self.game.Board.Board = [[0] * self.Cols for _ in range(self.Rows)]

        # Crear una superficie vacía para las imágenes de las piezas
        self.empty_surface = pygame.Surface((self.Square, self.Square))

    def test_castling(self):
        # Colocar las piezas en una posición inicial para enroque
        white_king = King(self.Square, self.empty_surface, White, "King", 7, 4)
        white_rook_king_side = Rook(self.Square, self.empty_surface, White, "Rook", 7, 7)
        white_rook_queen_side = Rook(self.Square, self.empty_surface, White, "Rook", 7, 0)

        self.game.Board.Board[7][4] = white_king
        self.game.Board.Board[7][7] = white_rook_king_side
        self.game.Board.Board[7][0] = white_rook_queen_side

        # Cambiar el turno a las blancas
        self.game.turn = White

        # Verificar enroque corto
        available_moves_king = white_king.move_strategy.get_available_moves(white_king, self.game.Board.Board)
        self.assertIn((7, 6), available_moves_king, "El enroque corto debería estar disponible")
        print("Enroque corto disponible")
        # Realizar el enroque corto
        self.game.Board.move(white_king, 7, 6)
        self.game.Board.move(white_rook_king_side, 7, 5)

        self.assertIsInstance(self.game.Board.Board[7][6], King, "El rey debería estar en la columna 6")
        self.assertIsInstance(self.game.Board.Board[7][5], Rook, "La torre debería estar en la columna 5")

        #reseteo el tablero
        white_king = King(self.Square, self.empty_surface, White, "King", 7, 4)
        white_rook_king_side = Rook(self.Square, self.empty_surface, White, "Rook", 7, 7)

        # Reset the board for the next test
        self.game.Board.Board[7][4] = white_king
        self.game.Board.Board[7][7] = white_rook_king_side
        self.game.Board.Board[7][6] = 0
        self.game.Board.Board[7][5] = 0

        # Verificar enroque largo
        available_moves_king = white_king.move_strategy.get_available_moves(white_king, self.game.Board.Board)
        self.assertIn((7, 2), available_moves_king, "El enroque largo debería estar disponible")
        print("Enroque largo disponible")
        # Realizar el enroque largo
        self.game.Board.move(white_king, 7, 2)
        self.game.Board.move(white_rook_queen_side, 7, 3)

        self.assertIsInstance(self.game.Board.Board[7][2], King, "El rey debería estar en la columna 2")
        self.assertIsInstance(self.game.Board.Board[7][3], Rook, "La torre debería estar en la columna 3")

if __name__ == "__main__":
    unittest.main()
