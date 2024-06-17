import pygame
from chess_game.controller import GameController
from chess_game.constants import *

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))

def get_positions(x, y):
    row = y // Square
    col = x // Square
    return row, col

def main_menu():
    font = pygame.font.SysFont('Arial', 72)
    run = True
    while run:
        Win.fill((0, 0, 0))

        # Dibujar texto "Jugar"
        play_text = font.render('Jugar', True, (255, 255, 255))
        play_rect = play_text.get_rect(center=(Width // 2, Height // 2 - 50))
        Win.blit(play_text, play_rect)

        # Dibujar texto "Salir"
        quit_text = font.render('Salir', True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(Width // 2, Height // 2 + 50))
        Win.blit(quit_text, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    run = False
                    main()
                if quit_rect.collidepoint(mouse_pos):
                    run = False
                    pygame.quit()
                    quit()

def main():
    run = True
    game_over = False
    FPS = 120
    game_controller = GameController(Width, Height, Rows, Cols, Square, Win)

    while run:
        clock.tick(FPS)
        game_controller.update()
        if game_controller.check_game():
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game_controller.reset()
                    game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if game_controller.board.promotion_choice:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if Width // 2 - 100 < mouse_x < Width // 2 + 100:
                        if Height // 2 - 100 < mouse_y < Height // 2 - 50:
                            game_controller.handle_promotion("Queen")
                        elif Height // 2 - 50 < mouse_y < Height // 2:
                            game_controller.handle_promotion("Rook")
                        elif Height // 2 < mouse_y < Height // 2 + 50:
                            game_controller.handle_promotion("Bishop")
                        elif Height // 2 + 50 < mouse_y < Height // 2 + 100:
                            game_controller.handle_promotion("Knight")
                else:
                    if pygame.mouse.get_pressed()[0]:
                        location = pygame.mouse.get_pos()
                        row, col = get_positions(location[0], location[1])
                        game_controller.select(row, col)

            if event.type == pygame.MOUSEMOTION and game_controller.board.promotion_choice:
                game_controller.update()

main_menu()
