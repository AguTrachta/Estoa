import pygame
import os
from Clases.Constantes import *

class Bishop:
    def __init__(self, Square, image, color, type, row, col):
        
        Black_Bishop = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "bB.png")), (Square, Square))
        White_bishop = pygame.transform.scale(pygame.image.load(os.path.join("Clases/Imagenes", "wB.png")), (Square, Square))

