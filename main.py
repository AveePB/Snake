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
pygame.display.set_icon(pygame.image.load(gui.SNAKE_IMG_PATH))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

# Initialize game parameters
gameplay = Gameplay()
appStage = Gameplay.AppStage.MENU
curr_gamemode = None

# Start the game
while True:
    # Exit app
    if appStage == Gameplay.AppStage.EXIT: break

    # Enter menu
    elif appStage == Gameplay.AppStage.MENU:
        # Draw menu
        gui.drawMenu(screen)
        pygame.display.flip()
        
        is_gameplay_picked = False
        gameplay.resetParameters()

        while not is_gameplay_picked:
            # Handle subevent
            for event in pygame.event.get():
                # User clicks X
                if event.type == pygame.QUIT:
                    appStage = Gameplay.AppStage.EXIT
                    is_gameplay_picked = True

                # User presses key
                elif event.type == pygame.KEYDOWN:
                    # Let User play
                    if event.key == pygame.K_0:
                        appStage = Gameplay.AppStage.GAME
                        curr_gamemode = Gameplay.Mode.PLAYER
                        is_gameplay_picked = True
                    
                    # Let AI play
                    elif event.key == pygame.K_1:
                        appStage = Gameplay.AppStage.GAME
                        curr_gamemode = Gameplay.Mode.AI
                        is_gameplay_picked = True
                    
                    # Let AI train
                    elif event.key == pygame.K_2:
                        appStage = Gameplay.AppStage.GAME
                        curr_gamemode = Gameplay.Mode.AI_TRAINING
                        is_gameplay_picked = True

    # Run game logic
    else:
        # Load neural network
        if curr_gamemode == Gameplay.Mode.AI:
            if os.path.exists(NN_MODEL_PATH): 
                gameplay.agent.model.load_state_dict(torch.load(NN_MODEL_PATH, weights_only=True))
                gameplay.agent.model.eval()
        
        # Start game
        appStage = gameplay.runLogic(curr_gamemode, screen)

    # Draw entities
    gameplay.draw(screen, curr_gamemode)

    #gui.drawMenu(screen)

    # Complete rendering 
    pygame.display.flip()
    
    # Set framerate
    if curr_gamemode == Gameplay.Mode.AI_TRAINING:
        clock.tick(TRAINING_FPS)
    else:
        clock.tick(GAME_FPS)

pygame.quit()