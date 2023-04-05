import gameplay.settings as sett
from gameplay.snake import Snake
from gameplay.food import Food

import pygame
import random
import math

class Game:
    def __init__(self) -> None:
        pygame.init()
        #initializes the "game over" sentences
        game_over_font = pygame.font.Font(sett.FONT_PATH, sett.FONT_GAME_OVER_SIZE)
        self.game_over_surf = game_over_font.render(sett.GAME_OVER, False, sett.FONT_COLOR)
        self.game_over_rect= self.game_over_surf.get_rect(center=(math.floor(sett.WIDTH/2), math.floor(sett.HEIGHT/2)))
        
        self.you_win_surf = game_over_font.render(sett.YOU_WIN, False, sett.FONT_COLOR)
        self.you_win_rect = self.you_win_surf.get_rect(center=(math.floor(sett.WIDTH/2), math.floor(sett.HEIGHT/2)))

        subsentence_font = pygame.font.Font(sett.FONT_PATH, math.floor(sett.FONT_GAME_OVER_SIZE/2))
        self.subsentence_surf = subsentence_font.render(sett.SUBSENTENCE, False, sett.FONT_COLOR)
        self.subsentence_rect = self.subsentence_surf.get_rect(midtop=(self.game_over_rect.centerx, self.game_over_rect.bottom))
        
        #creates the score and its font
        self.score_font = pygame.font.Font(sett.FONT_PATH, sett.FONT_SCORE_SIZE)
        self.score = 0        

        #forms the main window
        self.surf = pygame.display.set_mode((sett.WIDTH, sett.HEIGHT))
        pygame.display.set_caption(sett.TITLE)
        
        #sets basic parameters
        self.clock = pygame.time.Clock()
        self.state = False 
        # False <- Game remains
        # True <- Game Over

        #creates the fundamental gameplay objects
        self.player = Snake()

        x, y = self.findNewFruitPos()
        self.food = Food(x, y)
        

    def __isPosTaken(self, x: int, y: int) -> bool:
        #checks if the postion is occupied
        for rect in self.player.body_parts:
            if(rect.x == x*sett.TILE_SIZE and rect.y == y*sett.TILE_SIZE):
                return True
        return False

    def findNewFruitPos(self) -> tuple:
        x = 0
        y = 0
        while(True):
            x = math.floor(random.randint(0, sett.WIDTH)/sett.TILE_SIZE)
            y = math.floor(random.randint(0, sett.HEIGHT)/sett.TILE_SIZE)

            if(self.__isPosTaken(x, y)):
                continue
            break
        
        return (x*sett.TILE_SIZE, y*sett.TILE_SIZE)
        
    def run(self) -> None:
        while(True):
            #checks whether the event has occurred
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    exit()
                elif(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_SPACE and self.state):
                        #restarts the game
                        x, y = self.findNewFruitPos()
                        self.food = Food(x, y)
                        self.score = 0
                        
                        self.player = Snake()
                        self.state = False

            if(self.state):
                continue

            self.player.update()

            if(self.player.collision()):
                self.state = True

            if(self.player.eatFood(self.food.rect)):
                self.score += 1
                
                #checks if the player has won
                if(self.score+sett.SNAKE_START_LEN == (sett.WIDTH/sett.TILE_SIZE)*(sett.HEIGHT/sett.TILE_SIZE)):
                    self.state = True
                
                #spawns food out of the player's range
                if(self.state):
                    x = sett.WIDTH + 100
                    y = sett.HEIGHT + 100
                else:
                    x, y = self.findNewFruitPos()
                
                self.food = Food(x, y)
            
            #Draws the game objects 
            self.surf.fill(sett.BACKGROUND_COLOR)
            self.player.draw(self.surf)
            self.food.draw(self.surf) 

            #Displays the score
            score_surf = self.score_font.render(("Score: " + str(self.score)), False, sett.FONT_COLOR)
            score_rect = score_surf.get_rect(topright=(sett.WIDTH-sett.SCORE_POS, sett.SCORE_POS))
            self.surf.blit(score_surf, score_rect)
            
            #checks if the game is over
            if(self.state):
                if(self.score+sett.SNAKE_START_LEN == (sett.WIDTH/sett.TILE_SIZE)*(sett.HEIGHT/sett.TILE_SIZE)):
                    self.surf.blit(self.you_win_surf, self.you_win_rect)
                else:
                    self.surf.blit(self.game_over_surf, self.game_over_rect)

                self.surf.blit(self.subsentence_surf, self.subsentence_rect)

            pygame.display.update()
            self.clock.tick(sett.MAX_FPS)
    