import gameplay.settings as sett
import pygame

class Food:
    def __init__(self, x: int, y: int) -> None:
        #initializes the surface and its position
        self.surf = pygame.surface.Surface((sett.TILE_SIZE, sett.TILE_SIZE))
        self.rect = self.surf.get_rect(topleft=(x, y))
        
        #sets the surface color
        self.surf.fill(sett.FOOD_COLOR) 

    def draw(self, parent_surf: pygame.surface.Surface) -> None:
        #draws food on the parent surface
        parent_surf.blit(self.surf, self.rect)