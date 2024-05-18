import pygame
import os

class Pawn:
    Black_pawn = None
    White_pawn = None

    @classmethod
    def load_images(cls, square_size):
        cls.Black_pawn = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "bP.png")), (square_size, square_size))
        cls.White_pawn = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "wp.png")), (square_size, square_size))

    def __init__(self, Square, color, type, row, col):
        self.Square = Square
        self.image = Pawn.Black_pawn if color == "Black" else Pawn.White_pawn
        self.color = color
        self.type = type
        self.row = row
        self.col = col