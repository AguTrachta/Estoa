import pygame
import os
from Clases.Constantes import *

class Bishop:
    def __init__(self, Square, image, color, type, row, col):
        
        Black_Knight = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes","bKN.png")), (Square, Square))
        White_Knight = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "wKN.png")), (Square, Square))
