import unittest
import pygame
from ..chess_game.Pieces import King, Queen, Rook
from ..chess_game.constants import White, Black
from ..chess_game.game import Game
from ..chess_game.board import newBoard

class TestCheckmate(unittest.TestCase):
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

    def test_checkmate(self):
        # Colocar las piezas en una situación de jaque mate
        # Rey negro en (7, 4)
        # Reina blanca en (6, 2)
        # Torre blanca en (7, 0)
        black_king = King(self.Square, self.empty_surface, Black, "King", 7, 4)
        white_queen = Queen(self.Square, self.empty_surface, White, "Queen", 6, 2)
        white_rook = Rook(self.Square, self.empty_surface, White, "Rook", 7, 0)

        self.game.Board.Board[7][4] = black_king
        self.game.Board.Board[6][2] = white_queen
        self.game.Board.Board[7][0] = white_rook

        # Cambiar el turno a las negras
        self.game.turn = Black

        # Comprobar que se detecta el jaque mate
        self.assertTrue(self.game.check_game())
        self.assertEqual(self.game.winner, "White wins")
        print(f"Winner: {self.game.winner}")

        # Verificar que se muestra el mensaje de jaque mate
        self.game.update_window()
        self.assertIsNotNone(self.game.winner)

if __name__ == "__main__":
    unittest.main()
