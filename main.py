from snake.consts import WINDOW_SIZE, FPS
from snake.game import Game, GameMode

import pygame

# Set game parameters
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
running = True
game = Game()

# Start the game
while running:
    # Close window
    if (game.getCurrMode() == GameMode.EXIT):
        running = False

    # Game is at menu point
    elif (game.getCurrMode() == GameMode.MENU):
        game.menu(screen)

    # Interaction with game
    else:
        game.run(screen) 

    # Complete rendering 
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()