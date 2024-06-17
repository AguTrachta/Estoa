import pygame
from .constants import *

class GameView:
    def __init__(self, win):
        self.win = win

    def draw_board(self, board):
        self.win.fill(CustomBrown)
        for row in range(board.Rows):
            for col in range(row % 2, board.Cols, 2):
                pygame.draw.rect(self.win, CustomBeige, (col * board.Square, row * board.Square, board.Square, board.Square))

    def draw_pieces(self, board):
        for row in range(board.Rows):
            for col in range(board.Cols):
                piece = board.Board[row][col]
                if piece != 0:
                    self.win.blit(piece.image, (piece.x, piece.y))

    def draw_available_moves(self, selected, valid_moves, square):
        if selected is not None:
            for pos in valid_moves:
                row, col = pos[0], pos[1]
                if selected.type == "King" and abs(selected.col - col) == 2:
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)

                pygame.draw.circle(self.win, color,
                                   (col * square + square // 2, row * square + square // 2),
                                   square // 8)

    def show_winner(self, winner):
        overlay = pygame.Surface((Width, Height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.win.blit(overlay, (0, 0))

        font = pygame.font.SysFont('Arial', 72, bold=True)
        text = font.render(winner, True, (255, 255, 255))
        text_rect = text.get_rect(center=(Width // 2, Height // 2))

        self.win.blit(text, text_rect)
        pygame.display.update()
        print(f"Winner displayed: {winner}")

    def show_promotion_choices(self):
        overlay = pygame.Surface((Width, Height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.win.blit(overlay, (0, 0))

        font = pygame.font.SysFont('Arial', 36, bold=True)
        choices = ["Queen", "Rook", "Bishop", "Knight"]
        choice_texts = [font.render(choice, True, (255, 255, 255)) for choice in choices]

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, text in enumerate(choice_texts):
            text_rect = text.get_rect(center=(Width // 2, Height // 2 - 75 + i * 50))

            if text_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.win, (150, 150, 150),
                                 text_rect.inflate(20, 10))

            self.win.blit(text, text_rect)

        pygame.display.update()
        print("Promotion choices displayed")
