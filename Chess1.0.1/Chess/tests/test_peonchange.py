import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from chess_game.game import Game
from chess_game.constants import White, Black
from chess_game.board import newBoard
from chess_game.Pieces import Pawn, Queen #Solo probamos el peon convirtiendose en reina.

class TestPawnPromotion(unittest.TestCase):

    def setUp(self):
        self.game = Game(680, 680, 8, 8, 680 // 8, None)

    def test_pawn_promotion(self):
        self.game.Board.Board[0][0] = Pawn(680 // 8, None, White, "Pawn", 0, 0)
        self.game.Board.promotion_choice = self.game.Board.Board[0][0]
        self.game.handle_promotion("Queen")
        self.assertIsInstance(self.game.Board.get_piece(0, 0), Queen)

    def test_pawn_promotion_black(self):
        self.game.Board.Board[7][0] = Pawn(680 // 8, None, Black, "Pawn", 7, 0)
        self.game.Board.promotion_choice = self.game.Board.Board[7][0]
        self.game.handle_promotion("Queen")
        self.assertIsInstance(self.game.Board.get_piece(7, 0), Queen)

if __name__ == "__main__":
    unittest.main()
