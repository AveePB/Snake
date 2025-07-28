from snake.game import Gameplay
import snake.gui as gui

import pygame
import torch
import os

# Constants
NN_MODEL_PATH = './assets/models/180.pth'
TRAINING_FPS = 100
GAME_FPS = 10

# Initialize screen
screen = pygame.display.set_mode(gui.WINDOW_SIZE)
pygame.display.set_caption('Snake AI Training')
clock = pygame.time.Clock()

# Initialize game parameters
gameplay = Gameplay()
curr_gamemode = Gameplay.Mode.AI_TRAINING
# Load neural network
if curr_gamemode == Gameplay.Mode.AI:
    if os.path.exists(NN_MODEL_PATH): 
        gameplay.agent.model.load_state_dict(torch.load(NN_MODEL_PATH, weights_only=True))
        gameplay.agent.model.eval()

# Start the game
while True:
    # Run logic
    if gameplay.runLogic(curr_gamemode):
        break

    # Draw entities
    gameplay.draw(screen, curr_gamemode)

    # Complete rendering 
    pygame.display.flip()

    # Set framerate
    if curr_gamemode == Gameplay.Mode.AI_TRAINING:
        clock.tick(TRAINING_FPS)
    else:
        clock.tick(GAME_FPS)

pygame.quit()