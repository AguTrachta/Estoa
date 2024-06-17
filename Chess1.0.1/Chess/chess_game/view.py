import pygame
from .constants import *

class GameView:
    def __init__(self, win):
        self.win = win
        self.background_image = pygame.image.load('Chess1.0.1/Chess/chess_game/chess_images/chess_image.webp')

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

    def draw_main_menu(self):
        self.win.blit(self.background_image, (0, 0))  # Dibujar la imagen de fondo

        # Dibujar el overlay oscuro
        overlay = pygame.Surface((Width, Height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.win.blit(overlay, (0, 0))

        font_title = pygame.font.SysFont('Arial', 100, bold=True)
        font_option = pygame.font.SysFont('Arial', 72, bold=True)
        
        # Dibujar título "Estoa Chess"
        title_text = font_title.render('Estoa Chess', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(Width // 2, Height // 2 - 200))
        self.win.blit(title_text, title_rect)

        # Dibujar texto "Jugar"
        play_text = font_option.render('Jugar', True, (255, 255, 255))
        play_rect = play_text.get_rect(center=(Width // 2, Height // 2 - 50))

        # Dibujar texto "Salir"
        quit_text = font_option.render('Salir', True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(Width // 2, Height // 2 + 50))

        # Efecto de hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if play_rect.collidepoint((mouse_x, mouse_y)):
            play_text = font_option.render('Jugar', True, (255, 0, 0))  # Color rojo en hover
        if quit_rect.collidepoint((mouse_x, mouse_y)):
            quit_text = font_option.render('Salir', True, (255, 0, 0))  # Color rojo en hover

        self.win.blit(play_text, play_rect)
        self.win.blit(quit_text, quit_rect)

        pygame.display.update()

        return play_rect, quit_rect
