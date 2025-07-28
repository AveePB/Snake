from snake.agent import Agent
import snake.sprite as sprite
import snake.gui as gui

from enum import Enum
import numpy as np
import random 
import pygame

NN_MODEL_NAME = '340.pth'

class Gameplay:

    class Direction(Enum):
        UP = 0,
        DOWN = 1,
        LEFT = 2,
        RIGHT = 3,
    
    class Mode(Enum):
        PLAYER = 0,
        AI = 1,
        AI_TRAINING = 2,

    def __init__(self):
        # Initialize snake with size 3
        self.snake = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2)
        self.snake_direction = random.choice([Gameplay.Direction.UP, Gameplay.Direction.DOWN, Gameplay.Direction.LEFT, Gameplay.Direction.RIGHT])

        # Set snake to go up
        if self.snake_direction == Gameplay.Direction.UP:
            self.snake.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 + 1, gui.N_COLS // 2)
            self.snake.next_sprite.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 + 2, gui.N_COLS // 2)

        # Set snake to go down
        elif self.snake_direction == Gameplay.Direction.DOWN:
            self.snake.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 - 1, gui.N_COLS // 2)
            self.snake.next_sprite.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 - 2, gui.N_COLS // 2)    
        
        # Set snake to go left
        elif self.snake_direction == Gameplay.Direction.LEFT:
            self.snake.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2 + 1)
            self.snake.next_sprite.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2 + 2)

        # Set snake to go right
        else:
            self.snake.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2 - 1)
            self.snake.next_sprite.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2 - 2)
        
        # Initialize apple
        self.apple = None
        self.spawnApple()

        # Initialize game parameters
        self.agent = Agent()
        self.score = 0
        self.record = 0

    def spawnApple(self):
        # Try to find free spot for apple
        while True:
            # Choose random position
            row = random.randint(0, gui.N_ROWS - 1)
            col = random.randint(0, gui.N_COLS - 1)

            is_collision = False
            root = self.snake

            # Check if apple collides with snake
            while root != None:
                if root.curr_row == row and root.curr_col == col:
                    is_collision = True
                    break
                root = root.next_sprite

            # Spawn apple if position is okay
            if not is_collision:
                self.apple = sprite.AppleSprite(row, col)
                break
    
    def readUserInput(self, playerMode = True):
        # Handle user input
        for event in pygame.event.get():
            # User clicks X
            if event.type == pygame.QUIT:
                return True
            
            # User controls snake
            elif playerMode and event.type == pygame.KEYDOWN:
                # Set snake direction to UP
                if event.key == pygame.K_UP:
                    self.snake_direction = Gameplay.Direction.UP

                # Set snake direction to DOWN
                elif event.key == pygame.K_DOWN:
                    self.snake_direction = Gameplay.Direction.DOWN

                # Set snake direction to LEFT
                elif event.key == pygame.K_LEFT:
                    self.snake_direction = Gameplay.Direction.LEFT
                
                # Set snake direction to RIGHT
                elif event.key == pygame.K_RIGHT:
                    self.snake_direction = Gameplay.Direction.RIGHT
        
        return False
    
    def readAgentInput(self, is_training):
        # Handle AI input
        state_old = self.agent.getState(self.snake_direction, self.snake, self.apple)
        action =  self.agent.getAction(state_old, is_training) # [forward_score, left_score, right_score]
        idx = np.argmax(action)

        # Snake moves up 
        if self.snake_direction == Gameplay.Direction.UP:
            # AI wants to go forward
            if idx == 0:
                self.snake_direction = Gameplay.Direction.UP
                
            # AI wants to go left
            elif idx == 1:
                self.snake_direction = Gameplay.Direction.LEFT
                
            # AI wants to go right
            else:
                self.snake_direction = Gameplay.Direction.RIGHT 

        # Snake moves down
        elif self.snake_direction == Gameplay.Direction.DOWN:
            # AI wants to go forward
            if idx == 0:
                self.snake_direction = Gameplay.Direction.DOWN
                
            # AI wants to go left
            elif idx == 1:
                self.snake_direction = Gameplay.Direction.RIGHT
                
            # AI wants to go right
            else:
                self.snake_direction = Gameplay.Direction.LEFT

        # Snake moves left
        elif self.snake_direction == Gameplay.Direction.LEFT:
            # AI wants to go forward
            if idx == 0:
                self.snake_direction = Gameplay.Direction.LEFT
                
            # AI wants to go left
            elif idx == 1:
                self.snake_direction = Gameplay.Direction.DOWN
                
            # AI wants to go right
            else:
                self.snake_direction = Gameplay.Direction.UP 

        # Snake moves right
        else:
            # AI wants to go forward
            if idx == 0:
                self.snake_direction = Gameplay.Direction.RIGHT
                
            # AI wants to go left
            elif idx == 1:
                self.snake_direction = Gameplay.Direction.UP
                
            # AI wants to go right
            else:
                self.snake_direction = Gameplay.Direction.DOWN

        return state_old, action
    
    def trainAgent(self, state_old, action, reward, state_new, is_gameover):
        # Train on short term memory
        state_new = self.agent.getState(self.snake_direction, self.snake, self.apple)
        self.agent.trainShortMemory(state_old, action, reward, state_new, is_gameover)
        self.agent.remember(state_old, action, reward, state_new, is_gameover)

        # Train on long term memory
        if is_gameover:
            self.agent.trainLongMemory()
            self.agent.n_games += 1

            # Save better model
            if self.score > self.record:
                self.record = self.score
                self.agent.model.save(f'{self.record}.pth')
        
    def runLogic(self, gamemode):
        state_old, action = None, None

        # User controls snake
        if gamemode == Gameplay.Mode.PLAYER:
            if self.readUserInput(playerMode=True): return True
        
        # AI controls snake
        elif gamemode == Gameplay.Mode.AI:
            if self.readUserInput(playerMode=False): return True
            self.readAgentInput(is_training=False)
        
        # AI trains
        else:
            if self.readUserInput(playerMode=False): return True
            state_old, action = self.readAgentInput(is_training=True) 

        # Snake moves up 
        if self.snake_direction == Gameplay.Direction.UP:
            self.snake.move(self.snake.curr_row - 1, self.snake.curr_col)
        
        # Snake moves down
        elif self.snake_direction == Gameplay.Direction.DOWN:
            self.snake.move(self.snake.curr_row + 1, self.snake.curr_col)
        
        # Snake moves left
        elif self.snake_direction == Gameplay.Direction.LEFT:
            self.snake.move(self.snake.curr_row, self.snake.curr_col - 1)
        
        # Snake moves right
        else:
            self.snake.move(self.snake.curr_row, self.snake.curr_col + 1)
        
        reward, is_gameover = 0, False
        
        # Snake out of bounds
        if (self.snake.curr_row < 0 or gui.N_ROWS <= self.snake.curr_row) or \
            (self.snake.curr_col < 0 or gui.N_COLS <= self.snake.curr_col):
            is_gameover = True
            reward = -10

        # Snake collision
        root = self.snake.next_sprite
        while root != None:
            if root.curr_row == self.snake.curr_row and root.curr_col == self.snake.curr_col:
                is_gameover = True
                reward = -10
                break
            root = root.next_sprite   

        # Snake consumes food
        if self.apple.row == self.snake.curr_row and self.apple.col == self.snake.curr_col:
            self.snake.grow()
            self.spawnApple()
            reward = 10
        
        # Update score
        self.score += reward
        
        # Train AI based on new/old state
        if gamemode == Gameplay.Mode.AI_TRAINING:
            state_new = self.agent.getState(self.snake_direction, self.snake, self.apple)
            self.trainAgent(state_old, action, reward, state_new, is_gameover)

        if is_gameover:
            self.resetParameters()
        
        return False
    
    def resetParameters(self):
        # Reset game parameters
        self.score = 0

        # Initialize snake with size 3
        self.snake = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2)
        self.snake.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 + 1, gui.N_COLS // 2)
        self.snake.next_sprite.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 + 2, gui.N_COLS // 2)
        self.snake_direction = Gameplay.Direction.UP
                
        # Initialize apple
        self.apple = None
        self.spawnApple()
        self.is_ai_training = False

    def draw(self, screen, gamemode):
        # Draw objects
        gui.drawBackground(screen)
        self.snake.draw(screen)
        self.apple.draw(screen)

        # Display score
        score_surf = gui.BIG_FONT.render(f"Score: {self.score}", True, 'white')
        screen.blit(score_surf, (gui.WINDOW_SIZE[0] - (score_surf.get_width() + gui.WINDOW_SIZE[0] // 20), 30))

        # Display AI training info
        if gamemode == Gameplay.Mode.AI_TRAINING:
            msg_surf = gui.MID_FONT.render('AI: Training', True, 'white')
            screen.blit(msg_surf, (10, 30))
        
        # Display AI playing info
        elif gamemode == Gameplay.Mode.AI:
            msg_surf = gui.MID_FONT.render('AI: Playing', True, 'white')
            screen.blit(msg_surf, (10, 30))
