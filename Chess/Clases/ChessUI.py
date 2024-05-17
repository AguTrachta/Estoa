import pygame
import os
import sys

from Clases.Piezas.Pawn import Pawn
from Clases.Piezas.Bishop import Bishop
from Clases.Piezas.Rook import Rook
from Clases.Piezas.Knight import Knight
from Clases.Piezas.King import King
from Clases.Piezas.Queen import Queen

class ChessUI:
    def __init__(self, window_width=600, window_height=600):
        # Inicialización de Pygame
        pygame.init()

        COLORES_PIEZAS = {
            "blanco": (255, 255, 255),  # Color blanco
            "negro": (0, 0, 0),          # Color negro
        }       

        # Dimensiones de la ventana
        self.window_width = window_width
        self.window_height = window_height

        # Definir colores
        self.WHITE = (255, 231, 186)  # Beige para los cuadrados blancos
        self.BLACK = (165, 113, 71)   # Marrón para los cuadrados negros

        # Crear ventana
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Tablero de Ajedrez")

        # Tamaño del cuadrado del tablero
        self.square_size = self.window_width // 8  

        # Directorio donde se encuentran las imágenes de las piezas
        self.images_dir = os.path.join("Clases", "Imagenes")
        
        #Tamaño de los peones
        self.pieces_size = (50, 50)  # Anchura y altura deseada para los peones
        
        #Peones
        self.pawn = Pawn()
        # Cargar imágenes de los peones blancos y negros y ajustar su tamaño
        self.white_pawn = pygame.transform.scale(self.pawn.image_white, self.pieces_size)
        self.black_pawn = pygame.transform.scale(self.pawn.image_black, self.pieces_size)
        
        #Torres
        self.rook = Rook()
        
        self.white_rook = pygame.transform.scale(self.rook.image_white, self.pieces_size)
        self.black_rook = pygame.transform.scale(self.rook.image_black, self.pieces_size)
        
        #Alfiles
        self.bishop = Bishop()
        
        self.white_bishop = pygame.transform.scale(self.bishop.image_white, self.pieces_size) 
        self.black_bishop = pygame.transform.scale(self.bishop.image_black, self.pieces_size) 

        #Caballos
        self.knight = Knight()
        
        self.white_knight = pygame.transform.scale(self.knight.image_white, self.pieces_size) 
        self.black_knight = pygame.transform.scale(self.knight.image_black, self.pieces_size) 
        
        #King
        self.king = King()
        
        self.white_king = pygame.transform.scale(self.king.image_white, self.pieces_size) 
        self.black_king= pygame.transform.scale(self.king.image_black, self.pieces_size) 
        
        #Queen
        self.queen = Queen()
        
        self.white_queen = pygame.transform.scale(self.queen.image_white, self.pieces_size) 
        self.black_queen = pygame.transform.scale(self.queen.image_black, self.pieces_size) 

    def draw_chessboard(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = self.WHITE
                else:
                    color = self.BLACK
                pygame.draw.rect(self.window, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw_pawns(self, COLORES_PIEZAS):
        for row in range(8):
            if row == 1:
                for col in range(8):
                    x = col * self.square_size + (self.square_size - self.pieces_size[0]) // 2
                    y = row * self.square_size + (self.square_size - self.pieces_size[0]) // 2 
                    color = COLORES_PIEZAS["blanca"]
                    self.window.blit(self.white_pawn, (x, y))
            elif row == 6:
                for col in range(8):
                    x = col * self.square_size + (self.square_size - self.pieces_size[0]) // 2
                    y = row * self.square_size + (self.square_size - self.pieces_size[1]) // 2
                    color = COLORES_PIEZAS["negra"]
                    self.window.blit(self.black_pawn, (x, y))
                    
    def draw_rooks(self, color):
            # Dibujar torres blancas en las esquinas superiores
        if color == "blanco":
            self.window.blit(self.white_rook, (self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            self.window.blit(self.white_rook, ((7 * self.square_size) + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            # Dibujar torres negras en las esquinas inferiores
        elif color == "negro":
            self.window.blit(self.black_rook, (self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))
            self.window.blit(self.black_rook, ((7 * self.square_size) + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))

    def draw_knights(self, color):
        if color == "blanco": 
            # Dibujar caballos blancos en las esquinas superiores
            self.window.blit(self.white_knight, (self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            self.window.blit(self.white_knight, ((6 * self.square_size) + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            # Dibujar caballos negros en las esquinas inferiores
        elif color == "negro":
            self.window.blit(self.black_knight, (self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))
            self.window.blit(self.black_knight, ((6 * self.square_size) + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))

    def draw_bishops(self, color):
            # Dibujar alfiles blancos en las esquinas superiores
        if color == "blanco": 
            self.window.blit(self.white_bishop, (2 * self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            self.window.blit(self.white_bishop, ((5 * self.square_size) + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            # Dibujar alfiles negros en las esquinas inferiores
        elif color == "negro":
            self.window.blit(self.black_bishop, (2 * self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))
            self.window.blit(self.black_bishop, ((5 * self.square_size) + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))
        
    def draw_queen(self, color):
            # Dibujar reinas blancos en las esquinas superiores
        if color == "blanco":
            self.window.blit(self.white_queen, (3 * self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            # Dibujar reinas negros en las esquinas inferiores
        elif color == "negro":
            self.window.blit(self.black_queen, (3 * self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))

    def draw_king(self, color):
            # Dibujar reinas blancos en las esquinas superiores
        if color == "blanco":
            self.window.blit(self.white_king, (4 * self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, self.square_size // 2 - self.pieces_size[1] // 2))
            # Dibujar reinas negros en las esquinas inferiores
        elif color == "negro": 
            self.window.blit(self.black_king, (4 * self.square_size + self.square_size // 2 - self.pieces_size[0] // 2, (7 * self.square_size) + self.square_size // 2 - self.pieces_size[1] // 2))

    def run(self):
        # Bucle principal del juego
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Dibujar el tablero de ajedrez
            self.window.fill(self.WHITE)  # Llenar la ventana con color blanco
            self.draw_chessboard()

            # Dibujar peones en el tablero
            self.draw_pawns()
            self.draw_rooks("blanco")
            self.draw_rooks("negro")
            self.draw_knights("blanco")
            self.draw_knights("negro")
            self.draw_bishops("blanco")
            self.draw_bishops("negro")
            self.draw_queen("blanco")
            self.draw_king()

            # Actualizar la pantalla
            pygame.display.update()

                

        # Salir del programa
        pygame.quit()
        sys.exit()
