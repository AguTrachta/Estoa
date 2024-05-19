import pygame
from chess_game.constants import *
from chess_game.game import Game

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))

def get_positions(x, y):
    row = y // Square
    col = x // Square
    return row, col

def main():
    run = True
    game_over = False
    FPS = 60
    game = Game(Width, Height, Rows, Cols, Square, Win)

    while run:
        clock.tick(FPS)
        game.update_window()
        if game.check_game():
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if game.Board.promotion_choice:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Definir las áreas de clic para cada opción
                    if Width // 2 - 100 < mouse_x < Width // 2 + 100:
                        if Height // 2 - 100 < mouse_y < Height // 2 - 50:
                            game.handle_promotion("Queen")
                        elif Height // 2 - 50 < mouse_y < Height // 2:
                            game.handle_promotion("Rook")
                        elif Height // 2 < mouse_y < Height // 2 + 50:
                            game.handle_promotion("Bishop")
                        elif Height // 2 + 50 < mouse_y < Height // 2 + 100:
                            game.handle_promotion("Knight")
                else:
                    if pygame.mouse.get_pressed()[0]:
                        location = pygame.mouse.get_pos()
                        row, col = get_positions(location[0], location[1])
                        game.select(row, col)

            if event.type == pygame.MOUSEMOTION and game.Board.promotion_choice:
                game.update_window()  # Actualizar la ventana para reflejar el efecto de hover

main()
