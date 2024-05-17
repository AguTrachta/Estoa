import pygame

from Clases.Piezas.Pawn import Pawn
from Clases.Piezas.Bishop import Bishop
from Clases.Piezas.Rook import Rook
from Clases.Piezas.Knight import Knight
from Clases.Piezas.King import King
from Clases.Piezas.Queen import Queen

class Movimiento:
    
    def __init__ (self, pieza, posicion): 
        self.pieza = pieza
        self.posicion = posicion
        self.posibles_movimientos = self.calcular_posibles_movimientos()
        
        
        
    def calcular_posibles_movimientos(self, color):
        if self.pieza == Pawn:
            return self.calcular_movimientos_pawn()
        
    def calcular_movimientos_pawn(self):
        # Implementa la lógica para calcular los movimientos de un peón
        pass
