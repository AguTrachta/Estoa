import unittest
from ..chess_game.Pieces import Pawn, Rook, Bishop, Knight, Queen, King

class TestPieces(unittest.TestCase):
    def setUp(self):
        self.Square = 60
        self.image = None
        self.white_pawn = Pawn(self.Square, self.image, "White", "Pawn", 6, 0)
        self.black_pawn = Pawn(self.Square, self.image, "Black", "Pawn", 1, 0)
        self.board = [[0]*8 for _ in range(8)]
        self.board[6][0] = self.white_pawn
        self.board[1][0] = self.black_pawn

    def test_pawn_moves(self):
        moves = self.white_pawn.get_available_moves(6, 0, self.board)
        print("Available moves for white pawn:", moves)  # Agrega una impresión para depuración
        self.assertIn((5, 0), moves)
        self.assertIn((4, 0), moves)

if __name__ == "__main__":
    unittest.main()
