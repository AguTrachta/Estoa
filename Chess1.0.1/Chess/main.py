import pygame
from chess_game.controller import GameController
from chess_game.constants import *

pygame.init()
clock = pygame.time.Clock()

# Aumentar la pantalla para acomodar los temporizadores
Width, Height = 800, 680  # Ajusta el tamaño según sea necesario
Win = pygame.display.set_mode((Width + 200, Height))

def get_positions(x, y):
    row = y // Square
    col = x // Square
    return row, col

def main():
    run = True
    game_over = False
    FPS = 120
    game_controller = GameController(Width, Height, Rows, Cols, Square, Win)

    while run:
        clock.tick(FPS)
        if not game_over:
            resign_rect = game_controller.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game_controller.reset()
                    game_over = False
                    game_controller.winner_displayed = False  # Reiniciamos la bandera

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_controller.in_menu:
                    game_controller.handle_menu_click(mouse_pos)
                elif not game_over:
                    if resign_rect and resign_rect.collidepoint(mouse_pos):
                        game_controller.handle_resign()
                        game_over = True
                    elif game_controller.board.promotion_choice:
                        if Width // 2 - 100 < mouse_pos[0] < Width // 2 + 100:
                            if Height // 2 - 100 < mouse_pos[1] < Height // 2 - 50:
                                game_controller.handle_promotion("Queen")
                            elif Height // 2 - 50 < mouse_pos[1] < Height // 2:
                                game_controller.handle_promotion("Rook")
                            elif Height // 2 < mouse_pos[1] < Height // 2 + 50:
                                game_controller.handle_promotion("Bishop")
                            elif Height // 2 + 50 < mouse_pos[1] < Height // 2 + 100:
                                game_controller.handle_promotion("Knight")
                    else:
                        if pygame.mouse.get_pressed()[0]:
                            row, col = get_positions(mouse_pos[0], mouse_pos[1])
                            game_controller.select(row, col)

            if event.type == pygame.MOUSEMOTION and game_controller.board.promotion_choice:
                game_controller.update()

main()
