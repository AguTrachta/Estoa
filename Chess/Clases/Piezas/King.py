import pygame
import os
from Clases.Constantes import *

class King:
    def __init__(self, Square, image, color, type, row, col):
        
        Black_King = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "bK.png")), (Square, Square))
        White_King = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "wK.png")), (Square, Square))
