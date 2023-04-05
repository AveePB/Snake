import gameplay.settings as sett
import pygame
import random
import math

class Snake:
    def __init__(self) -> None:
        #initializes the surface and sets its color
        self.surf = pygame.surface.Surface((sett.TILE_SIZE, sett.TILE_SIZE))
        self.surf.fill(sett.SNAKE_COLOR)

        #forms the initial body
        self.body_parts = []
        head_x = ((math.floor(sett.WIDTH/(sett.TILE_SIZE*2)))*sett.TILE_SIZE)
        head_y = ((math.floor(sett.HEIGHT/(sett.TILE_SIZE*2)))*sett.TILE_SIZE)
        for i in range(sett.SNAKE_START_LEN):
            self.body_parts.append(self.surf.get_rect(topleft=(head_x, head_y+sett.TILE_SIZE*i)))
        
        #chooses random beginning direction and creates an empty tail position
        self.direction = random.choice([sett.UP, sett.LEFT, sett.RIGHT])
        self.tail_pos = ()

    def move(self) -> None:
        #sets the new tail position
        self.tail_pos = self.body_parts[len(self.body_parts)-1].x, self.body_parts[len(self.body_parts)-1].y
        
        #changes the body position
        for i in range(len(self.body_parts)-1, 0, -1):
            self.body_parts[i].x = self.body_parts[i-1].x
            self.body_parts[i].y = self.body_parts[i-1].y
        
        #sets the new head position
        if(self.direction == sett.UP):
            self.body_parts[0].y -= sett.TILE_SIZE
        elif(self.direction == sett.DOWN):
            self.body_parts[0].y += sett.TILE_SIZE
        elif(self.direction == sett.LEFT):
            self.body_parts[0].x -= sett.TILE_SIZE
        elif(self.direction == sett.RIGHT):
            self.body_parts[0].x += sett.TILE_SIZE

    def userInput(self) -> None:
        keys = pygame.key.get_pressed()

        #sets a new direction for the snake
        if(keys[pygame.K_UP] and self.direction != sett.DOWN):
            self.direction = sett.UP
        elif(keys[pygame.K_DOWN] and self.direction != sett.UP):
            self.direction = sett.DOWN
        elif(keys[pygame.K_LEFT] and self.direction != sett.RIGHT):
            self.direction = sett.LEFT
        elif(keys[pygame.K_RIGHT] and self.direction != sett.LEFT):
            self.direction = sett.RIGHT
    
    def collision(self) -> bool:
        #checks whether a body collision has occurred
        for i in range(1, len(self.body_parts)):
            if(self.body_parts[0].colliderect(self.body_parts[i])):
                return True
        
        #checks if the snake is out of area
        if(self.body_parts[0].x < 0): #LEFT
            return True
        if(self.body_parts[0].x > sett.WIDTH-sett.TILE_SIZE): #RIGHT
            return True
        if(self.body_parts[0].y < 0): #TOP
            return True
        if(self.body_parts[0].y > sett.HEIGHT-sett.TILE_SIZE): #BOTTOM
            return True
        return False

    def eatFood(self, food_rect: pygame.rect.Rect) -> None:
        #checks if the food has been eaten
        if(self.body_parts[0].colliderect(food_rect)):
            self.body_parts.append(self.surf.get_rect(topleft=self.tail_pos))
        return self.body_parts[0].colliderect(food_rect)

    def update(self) -> None:
        self.userInput()
        self.move()
    
    def draw(self, parent_surf: pygame.surface.Surface) -> None:
        #draws a snake on the parent surface
        for rect in self.body_parts:
            parent_surf.blit(self.surf, rect)