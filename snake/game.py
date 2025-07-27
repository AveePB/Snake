import snake.sprite as sprite
import snake.gui as gui

from enum import Enum
import random 
import pygame

class Gameplay:

    class Direction(Enum):
        UP = 0,
        DOWN = 1,
        LEFT = 2,
        RIGHT = 3,

    def __init__(self):
        # Initialize snake with size 3
        self.snake = sprite.SnakeSprite(gui.N_ROWS // 2, gui.N_COLS // 2)
        self.snake.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 + 1, gui.N_COLS // 2)
        self.snake.next_sprite.next_sprite = sprite.SnakeSprite(gui.N_ROWS // 2 + 2, gui.N_COLS // 2)
        self.snake_direction = Gameplay.Direction.UP

        # Initialize apple
        self.apple = None
        self.spawnApple()

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
        
    def runLogic(self, playerMode = True):
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
        
        # Handle AI input
        if not playerMode:
            ...

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
        
        is_gameover = False
        
        # Snake out of bounds
        if (self.snake.curr_row < 0 or gui.N_ROWS <= self.snake.curr_row) or \
            (self.snake.curr_col < 0 or gui.N_COLS <= self.snake.curr_col):
            is_gameover = True

        # Snake collision
        root = self.snake.next_sprite
        while root != None:
            if root.curr_row == self.snake.curr_row and root.curr_col == self.snake.curr_col:
                is_gameover = True
                break
            root = root.next_sprite   

        # Snake consumes food
        if self.apple.row == self.snake.curr_row and self.apple.col == self.snake.curr_col:
            self.snake.grow()
            self.spawnApple()

        # Train AI
        if not playerMode:
            ...
            
            # Reset game parameters
            if is_gameover:
                is_gameover = False
                self.__init__()
        
        return is_gameover
    
    def draw(self, screen):
        gui.drawBackground(screen)
        self.snake.draw(screen)
        self.apple.draw(screen)
