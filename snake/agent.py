from collections import deque
from snake.model import Linear_QNet, QTrainer
from snake.gui import N_ROWS, N_COLS

import numpy as np
import torch
import random

N_TRAININGS = 200
MAX_MEMORY = 100_000
BATCH_SIZE = 1000

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        
        self.model = Linear_QNet()
        self.trainer = QTrainer(self.model)

    def getState(self, snake_direction, snake, apple):

        def isObstacle(snake, row, col):
            # row/col is out of bounds
            if (row < 0 or N_ROWS <= row) or \
                (col < 0 or N_COLS <= col):
                return True

            # Check if there is nearby snake body
            root = snake   
            while root != None:
                if root.curr_row == row and root.curr_col == col:
                    return True
                root = root.next_sprite         
            
            return False
        
        # Map current snake direction
        dir_up = snake_direction.value[0] == 0
        dir_down = snake_direction.value[0] == 1
        dir_left = snake_direction.value[0] == 2
        dir_right = snake_direction.value[0] == 3

        # Fetch snake position
        row, col = snake.curr_row, snake.curr_col

        state = [
            # Obstacle straight
            (dir_right and isObstacle(snake, row, col + 1)) or \
            (dir_left and isObstacle(snake, row, col - 1)) or \
            (dir_up and isObstacle(snake, row - 1, col)) or \
            (dir_down and isObstacle(snake, row + 1, col)),
        
            # Obstacle left
            (dir_right and isObstacle(snake, row - 1, col)) or \
            (dir_left and isObstacle(snake, row + 1, col)) or \
            (dir_up and isObstacle(snake, row, col - 1)) or \
            (dir_down and isObstacle(snake, row, col + 1)),

            # Obstacle right
            (dir_right and isObstacle(snake, row + 1, col)) or \
            (dir_left and isObstacle(snake, row - 1, col)) or \
            (dir_up and isObstacle(snake, row, col + 1)) or \
            (dir_down and isObstacle(snake, row, col - 1)),

            # Current direction
            dir_up,
            dir_down,
            dir_left,
            dir_right,

            # Food location
            apple.row < snake.curr_row,
            apple.row > snake.curr_row,
            apple.col < snake.curr_col,
            apple.col > snake.curr_col,
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, is_gameover):
        self.memory.append((state, action, reward, next_state, is_gameover))
    
    def trainShortMemory(self, state, action, reward, next_state, is_gameover):
        self.trainer.train_step(state, action, reward, next_state, is_gameover)

    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            samples = random.sample(self.memory, BATCH_SIZE)
        else:
            samples = self.memory
        
        states, actions, rewards, next_states, is_gameovers = zip(*samples)
        self.trainer.train_step(states, actions, rewards, next_states, is_gameovers)

    def getAction(self, state, is_training):
        self.epsilon = N_TRAININGS - self.n_games
        final_move = [0, 0, 0] # forward, left, right

        if not is_training: self.epsilon = 1

        # Exploration
        if random.randint(0, N_TRAININGS) <= self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        
        # Exploitation
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return np.array(final_move)