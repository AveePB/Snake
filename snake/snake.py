from snake.consts import TILE_SIZE, SNAKE_INIT_POS
from snake.sprites import SnakeBody, SnakeDirection, SnakeBodyPart, SnakeEvent

import random
import pygame

class Snake:
    """
    Represents the snake entity composed of different parts: head, body, and tail.
    Handles movement, growth, collision detection, and drawing.
    """
    
    def __init__(self, gameMap):
        """
        Initializes the snake object with a size of 3 (head, body, tail), positioned based on (x, y),
        and facing in a random starting direction.

        Args:
            gameMap (list[listp[int]]): numerical representation of current situation in the game.
        """
        self.__gameMap = gameMap

        # Random initial direction
        self.__currDirection = random.choice([
            SnakeDirection.UP, 
            SnakeDirection.DOWN, 
            SnakeDirection.LEFT, 
            SnakeDirection.RIGHT
        ])
        
        # Determine body/tail positioning based on direction
        x, y = SNAKE_INIT_POS[0], SNAKE_INIT_POS[1]
                
        if self.__currDirection is SnakeDirection.UP:
            body_x, body_y = x, y + TILE_SIZE
            tail_x, tail_y = x, y + 2 * TILE_SIZE
        elif self.__currDirection == SnakeDirection.DOWN:
            body_x, body_y = x, y - TILE_SIZE
            tail_x, tail_y = x, y - 2 * TILE_SIZE
        elif self.__currDirection == SnakeDirection.LEFT:
            body_x, body_y = x + TILE_SIZE, y
            tail_x, tail_y = x + 2 * TILE_SIZE, y
        else:  # RIGHT
            body_x, body_y = x - TILE_SIZE, y
            tail_x, tail_y = x - 2 * TILE_SIZE, y

        # Create parts
        self.__head = SnakeBody(x, y, SnakeBodyPart.HEAD, gameMap)
        body = SnakeBody(body_x, body_y, SnakeBodyPart.BODY, gameMap)
        tail = SnakeBody(tail_x, tail_y, SnakeBodyPart.TAIL, gameMap)

        # Link parts
        self.__head.set_next_body_part(body)
        body.set_next_body_part(tail)

        # Store non-head parts in group for rendering/collision
        self.__snake_body_group = pygame.sprite.Group()
        self.__snake_body_group.add(body, tail)

    def draw(self, screen):
        """
        Draws the entire snake on the screen.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        """
        screen.blit(self.__head.image, self.__head.rect)
        self.__snake_body_group.draw(screen)

    def move(self):
        """
        Moves the snake one block in the current direction.
        The head moves, and body parts follow automatically via set_pos().
        """
        x, y = self.__head.rect.topleft

        if self.__currDirection is SnakeDirection.UP:
            self.__head.set_pos((x, y - TILE_SIZE))
        elif self.__currDirection is SnakeDirection.DOWN:
            self.__head.set_pos((x, y + TILE_SIZE))
        elif self.__currDirection is SnakeDirection.LEFT:
            self.__head.set_pos((x - TILE_SIZE, y))
        elif self.__currDirection is SnakeDirection.RIGHT:
            self.__head.set_pos((x + TILE_SIZE, y))

    def set_direction(self, direction):
        """
        Updates the snake's direction, ignoring reverse-direction inputs.

        Args:
            direction (SnakeDirection): The new direction to set.
        """
        # Prevent reverse movement
        if (self.__currDirection == SnakeDirection.UP and direction == SnakeDirection.DOWN) or \
           (self.__currDirection == SnakeDirection.DOWN and direction == SnakeDirection.UP) or \
           (self.__currDirection == SnakeDirection.LEFT and direction == SnakeDirection.RIGHT) or \
           (self.__currDirection == SnakeDirection.RIGHT and direction == SnakeDirection.LEFT):
            return

        self.__currDirection = direction

    def handleEvents(self, apples, bounds):
        """
        Handles snake-related events: eating apples, self-collision, out-of-bounds.

        Args:
            apples (pygame.sprite.Group): Group of apple sprites.
            bounds (tuple[int, int]): Screen width and height.

        Returns:
            SnakeEvent: Enum indicating what happened (if anything).
        """
        # Apple collision check
        collided_apples = pygame.sprite.spritecollide(self.__head, apples, dokill=True)
        
        for collided_apple in collided_apples:
            x = collided_apple.rect.topleft[0]
            y = collided_apple.rect.topleft[1]

            collided_apple.update_game_map(True)

            # Promote current head to body
            old_head = self.__head
            old_head.set_texture(SnakeBodyPart.BODY)
            self.__snake_body_group.add(old_head)

            # Create new head and link
            self.__head = SnakeBody(x, y, SnakeBodyPart.HEAD, self.__gameMap)
            self.__head.set_next_body_part(old_head)

        if collided_apples:
            return SnakeEvent.SCORE_UPDATE

        # Self-collision
        collided_snake_parts = pygame.sprite.spritecollide(self.__head, self.__snake_body_group, dokill=False)
        if collided_snake_parts:
            return SnakeEvent.GAME_OVER

        # Out of bounds check
        head_x = self.__head.rect.topleft[0]
        head_y = self.__head.rect.topleft[1]

        if head_x < 0 or head_x >= bounds[0] or head_y < 0 or head_y >= bounds[1]:
            return SnakeEvent.GAME_OVER

        return SnakeEvent.NO_EVENT
