from snake.gui import TILE_SIZE, TEXTURE_SIZE
import random
import pygame

R_APPLE_TEXTURE = './assets/texture/red-apple.png'
G_APPLE_TEXTURE = './assets/texture/green-apple.png'
Y_APPLE_TEXTURE = './assets/texture/yellow-apple.png'
SNAKE_TEXTURE = './assets/texture/snake.png'

class AppleSprite(pygame.sprite.Sprite):
    
    def __init__(self, row, col):
        super().__init__()

        # Load rectangle and texture
        self.image = pygame.image.load(random.choice([R_APPLE_TEXTURE, G_APPLE_TEXTURE, Y_APPLE_TEXTURE])).convert_alpha()
        self.image = pygame.transform.scale(self.image, TEXTURE_SIZE)

        self.rect = self.image.get_rect()
        self.rect.topleft = (col*TILE_SIZE, row*TILE_SIZE)

        # Save info about position
        self.row = row
        self.col = col
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SnakeSprite(pygame.sprite.Sprite):

    def __init__(self, row, col):
        super().__init__()

        # Load rectangle and texture
        self.image = pygame.image.load(SNAKE_TEXTURE).convert_alpha()
        self.image = pygame.transform.scale(self.image, TEXTURE_SIZE)

        self.rect = self.image.get_rect()
        self.rect.topleft = (col*TILE_SIZE, row*TILE_SIZE)

        # Save info about position
        self.curr_row = row
        self.curr_col = col

        self.prev_row = None
        self.prev_col = None

        # Save info about snake's body
        self.next_sprite = None


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        # Draw next body part
        if self.next_sprite != None:
            self.next_sprite.draw(screen)
    
    def move(self, row, col):
        # Save old position
        self.prev_row = self.curr_row
        self.prev_col = self.curr_col

        # Set new position
        self.rect.topleft = (col*TILE_SIZE, row*TILE_SIZE)
        self.curr_row = row
        self.curr_col = col 

        # Move next body part
        if self.next_sprite != None:
            self.next_sprite.move(self.prev_row, self.prev_col)
    
    def grow(self):
        # It's not tail        
        if self.next_sprite != None:
            self.next_sprite.grow()
        
        # It's tail
        else:
            self.next_sprite = SnakeSprite(self.prev_row, self.prev_col)