import os
import pygame

# Definir constantes
label_space=50
Rows, Cols = 8, 8
Square = 80
Width = Cols * Square + 2 * label_space
Height = Rows * Square + 2 * label_space


# Definir colores
White = (255, 255, 255)
Black = (0, 0, 0)
CustomBrown = (181, 136, 99)
CustomBeige = (240, 217, 181)
Green = (0, 255, 0)
Red = (255, 0, 0)

# Ruta absoluta a la carpeta de imágenes
base_path = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(base_path, "chess_images")

# Cargar imágenes
Black_Pawn = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "bP.png")), (Square, Square))
White_Pawn = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "wp.png")), (Square, Square))
Black_Rook = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "bR.png")), (Square, Square))
White_Rook = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "wR.png")), (Square, Square))
Black_Knight = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "bKN.png")), (Square, Square))
White_Knight = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "wKN.png")), (Square, Square))
Black_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "bB.png")), (Square, Square))
White_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "wB.png")), (Square, Square))
Black_Queen = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "bQ.png")), (Square, Square))
White_Queen = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "wQ.png")), (Square, Square))
Black_King = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "bK.png")), (Square, Square))
White_King = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "wK.png")), (Square, Square))
