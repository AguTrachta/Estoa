import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from chess_game.game import Game
from chess_game.constants import White, Black
from chess_game.board import newBoard
from chess_game.Pieces import Pawn, Queen, Knight, Bishop, Rook

class TestPawnPromotion(unittest.TestCase):

    def setUp(self):
        self.game = Game(680, 680, 8, 8, 680 // 8, None)

    def test_pawn_promotion_1(self):
        self.game.Board.Board[0][0] = Pawn(680 // 8, None, White, "Pawn", 0, 0) #Ubico peon en 'a8'
        self.game.Board.promotion_choice = self.game.Board.Board[0][0] #Panel de eleccion de piezas a transformar
        self.game.handle_promotion("Queen") #Transformo en reina
        self.assertIsInstance(self.game.Board.get_piece(0, 0), Queen) #Aseguro que exista una reina en 'a8' 
        print("----------------------------------------------------------------------")
        print("El peon blanco en 'a8' se convirtio en Reina")
        
    def test_pawn_promotion_2(self):
        self.game.Board.Board[0][7] = Pawn(680 // 8, None, White, "Pawn", 0, 7)
        self.game.Board.promotion_choice = self.game.Board.Board[0][7]
        self.game.handle_promotion("Rook")
        self.assertIsInstance(self.game.Board.get_piece(0, 7), Rook)       

        print("El peon blanco en 'h8' se convirtio en Torre")

    def test_pawn_promotion_black(self):
        self.game.Board.Board[7][0] = Pawn(680 // 8, None, Black, "Pawn", 7, 0)
        self.game.Board.promotion_choice = self.game.Board.Board[7][0]
        self.game.handle_promotion("Knight")
        self.assertIsInstance(self.game.Board.get_piece(7, 0), Knight)
        print("El peon negro en 'a1' se convirtio en Caballo" )

    def test_pawn_promotion_black_2(self):
        self.game.Board.Board[7][7] = Pawn(680 // 8, None, Black, "Pawn", 7, 7)
        self.game.Board.promotion_choice = self.game.Board.Board[7][7]
        self.game.handle_promotion("Bishop")
        self.assertIsInstance(self.game.Board.get_piece(7, 7), Bishop)
        print("El peon negro en 'h1' se convirtio en Alfil" )
        
if __name__ == "__main__":
    unittest.main()
