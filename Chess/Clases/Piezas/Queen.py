import pygame
import os
from Clases.Constantes import *

class Queen:
    def __init__(self, Square, image, color, type, row, col):
        
        Black_Queen = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "bQ.png")), (Square, Square))
        White_Queen = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "wQ.png")), (Square, Square))
