import pygame
import os
from Clases.Constantes import *

class Rook:
    def __init__(self, Square, image, color, type, row, col):
        
        Black_Rook = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "bR.png")), (Square, Square))
        White_Rook = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "wR.png")), (Square, Square))

