import pygame
import os

class Bishop:
    def __init__(self, color):
        self.color = color
        self.images_dir = os.path.join("Clases", "Imagenes")
        self.image_white = pygame.image.load(os.path.join(self.images_dir, "white bishop.png"))
        self.image_black = pygame.image.load(os.path.join(self.images_dir, "black bishop.png"))