from snake.game import Gameplay
import snake.gui as gui
import pygame

# Set game parameters
screen = pygame.display.set_mode(gui.WINDOW_SIZE)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

gameplay = Gameplay()

# Start the game
while True:
    # Close application
    if gameplay.runLogic(False):
        break

    gameplay.draw(screen)

    # Complete rendering 
    pygame.display.flip()
    clock.tick(10)

pygame.quit()