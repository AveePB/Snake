from snake.consts import TEXTURE_SIZE, TILE_SIZE, OBSTACLE_HASH, HEAD_HASH, NO_HASH, APPLE_HASH

from enum import Enum
import pygame
import random

class Apple(pygame.sprite.Sprite):
    """
    Represents an apple sprite that randomly selects a color (red, green, or yellow)
    and displays the corresponding image at a specified (x, y) position.
    """

    def __init__(self, x, y, gameMap):
        """
        Initializes an Apple sprite at the given coordinates.

        Args:
            x (int): X-coordinate for the top-left of the apple sprite.
            y (int): Y-coordinate for the top-left of the apple sprite.
            gameMap (list[listp[int]]): numerical representation of current situation in the game.
        """
        super().__init__()

        # Randomly select a color for the apple
        color = random.choice(['red', 'green', 'yellow'])

        # Load the appropriate image based on the selected color
        if color == 'red':
            self.image = pygame.image.load('./assets/texture/red-apple.png').convert_alpha()
        elif color == 'green':
            self.image = pygame.image.load('./assets/texture/green-apple.png').convert_alpha()
        else:
            self.image = pygame.image.load('./assets/texture/yellow-apple.png').convert_alpha()

        # Scale the image to the defined texture size
        self.image = pygame.transform.scale(self.image, TEXTURE_SIZE)

        # Set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.__gameMap = gameMap
        self.update_game_map()

    def update_game_map(self, deletion=False):
        """
        Updates the current game state.
        """
        x, y = self.rect.topleft
        
        if (deletion):
            self.__gameMap[y // TILE_SIZE + 1][x // TILE_SIZE + 1] = NO_HASH
        else:
            self.__gameMap[y // TILE_SIZE + 1][x // TILE_SIZE + 1] = APPLE_HASH

class SnakeBodyPart(Enum):
    """Enum representing parts of the snake."""
    HEAD = 0
    BODY = 1
    TAIL = 2
    
class SnakeDirection(Enum):
    """Enum representing directions of the snake."""
    UP = 1   
    DOWN = 2  
    LEFT = 3
    RIGHT = 4
    
class SnakeEvent(Enum):
    """Enum representing snake events."""
    SCORE_UPDATE = 1
    GAME_OVER = 2
    NO_EVENT = 3

class SnakeBody(pygame.sprite.Sprite):
    """
    Represents a single part of the snake (head, body, or tail).
    Handles drawing and positional linking to the next part.
    """
        
    def __init__(self, x, y, bodyPart, gameMap):
        """
        Initializes a SnakeBody sprite at the given coordinates with the given body type.

        Args:
            x (int): X-coordinate for the top-left of the sprite.
            y (int): Y-coordinate for the top-left of the sprite.
            bodyPart (SnakeBodyPart): The snake's body part type for texture.
            gameMap (list[listp[int]]): numerical representation of current situation in the game.
        """
        super().__init__()
        self.__gameMap = gameMap

        # Load image based on type
        self.image = None
        self.set_texture(bodyPart)  

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.__nextBodyPart = None
        self.update_game_map()

    def set_pos(self, coordinates):
        """
        Updates the current position of the body part and recursively updates the next part.

        Args:
            coordinates (tuple[int, int]): New (x, y) position.
        """
        old_coordinates = self.rect.topleft
        old_row, old_col = old_coordinates[1] // TILE_SIZE + 1, old_coordinates[0] // TILE_SIZE + 1
        self.__gameMap[old_row][old_col] = NO_HASH

        self.rect.topleft = coordinates
        new_row, new_col = coordinates[1] // TILE_SIZE + 1, coordinates[0] // TILE_SIZE + 1
        
        # Update game map
        self.update_game_map()

        # Update next part to follow this part
        if self.__nextBodyPart:
            self.__nextBodyPart.set_pos(old_coordinates)
        
    def set_texture(self, bodyPart):
        """
        Updates the current texture of the body part.

        Args:
            bodyPart (SnakeBodyPart): Type of this body segment.
        """
        self.__bodyPart = bodyPart
        
        if bodyPart == SnakeBodyPart.HEAD:
            self.image = pygame.image.load('./assets/texture/snake-head.png').convert_alpha()
        elif bodyPart == SnakeBodyPart.BODY:
            self.image = pygame.image.load('./assets/texture/snake-body.png').convert_alpha()
        else:
            self.image = pygame.image.load('./assets/texture/snake-tail.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, TEXTURE_SIZE)

    def set_next_body_part(self, nextBodyPart):
        """
        Sets the reference to the next body part in the chain.

        Args:
            nextBodyPart (SnakeBody): The next SnakeBody part.
        """
        self.__nextBodyPart = nextBodyPart
    
    def update_game_map(self):
        """
        Updates the current game state.
        """
        x, y = self.rect.topleft

        if (self.__bodyPart == SnakeBodyPart.HEAD):
            self.__gameMap[y // TILE_SIZE + 1][x // TILE_SIZE + 1] = HEAD_HASH
        else:
            self.__gameMap[y // TILE_SIZE + 1][x // TILE_SIZE + 1] = OBSTACLE_HASH
