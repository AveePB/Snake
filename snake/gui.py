"""
Module contains draw methods that are useful to handle game drawings.
"""
import pygame
pygame.init()

# Color constants
DARK_BLUE = pygame.Color(2, 61, 163)
LIGHT_BLUE = pygame.Color(2, 40, 105)

# Size constants
N_ROWS = 20
N_COLS = 20
TILE_SIZE = 32
TEXTURE_SIZE = (TILE_SIZE, TILE_SIZE)
WINDOW_SIZE = (N_COLS * TILE_SIZE, N_ROWS * TILE_SIZE)
MENU_IMG_SIZE = (300, 300)

# Initialization of the game fonts
BIG_FONT = pygame.font.Font('./assets/font/game-font.ttf', size=20)
MID_FONT = pygame.font.Font('./assets/font/game-font.ttf', size=15)
SMALL_FONT = pygame.font.Font('./assets/font/game-font.ttf', size=10)

def drawBackground(screen):
    n_rows, n_cols = WINDOW_SIZE[1] // TILE_SIZE, WINDOW_SIZE[0] // TILE_SIZE
    isLight = True

    # Draw chess board
    for j in range(n_rows):
        # reset at the start of each row
        isLight = (j % 2 == 0)
        
        # Draw candy stick pattern
        for i in range(n_cols):
            color = LIGHT_BLUE if isLight else DARK_BLUE
            square_rect = (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            pygame.draw.rect(screen, color, square_rect)
            isLight = not isLight

def drawMenu(screen):
    # Create text labels
    title = BIG_FONT.render("Choose Game Mode", True, 'white')
    player_option = MID_FONT.render("Press SPACE to Play as Player", True, 'white')
    ai_option = MID_FONT.render("Press 0 to Train AI", True, 'white')
    menu_img = pygame.image.load('./assets/image/snake-menu.png')
    menu_img = pygame.transform.scale(menu_img, MENU_IMG_SIZE)

    # Draw elements
    drawBackground(screen)
    screen.blit(menu_img, (WINDOW_SIZE[0] // 2 - menu_img.get_width() // 2, 50))
    screen.blit(title, (WINDOW_SIZE[0] // 2 - title.get_width() // 2, 350))
    screen.blit(player_option, (WINDOW_SIZE[0] // 2 - player_option.get_width() // 2, 450))
    screen.blit(ai_option, (WINDOW_SIZE[0] // 2 - ai_option.get_width() // 2, 520))
