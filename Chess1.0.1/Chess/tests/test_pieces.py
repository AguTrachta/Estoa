import unittest
from Chess.chess_game.Pieces import Pawn, Rook, Bishop, Knight, Queen, King

class TestPieces(unittest.TestCase):
    def setUp(self):
        self.Square = 60
        self.image = None
        self.white_pawn = Pawn(self.Square, self.image, "White", "Pawn", 6, 0)
        self.black_pawn = Pawn(self.Square, self.image, "Black", "Pawn", 1, 0)
        self.board = [[0]*8 for _ in range(8)]

    def test_pawn_moves(self):
        moves = self.white_pawn.get_available_moves(6, 0, self.board)
        self.assertIn((5, 0), moves)
        self.assertIn((4, 0), moves)

if __name__ == "__main__":
    unittest.main()
