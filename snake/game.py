from snake.consts import WINDOW_SIZE, MENU_IMG_SIZE, APPLE_SPAWN_LIMIT, TILE_SIZE, OBSTACLE_HASH, APPLE_HASH, NO_HASH
from snake.snake import SnakeDirection, Snake
from snake.sprites import Apple, SnakeEvent

from enum import Enum
import random
import pygame

class GameMode(Enum):
    """Enum representing different game states."""
    MENU = 1
    GAME_PLAYER = 2
    GAME_AI = 3
    EXIT = 4

class Game:
    """
    Handels game dynamic and switching between game states.
    """

    def __init__(self):
        """
            It is responsible for initialization of the game.
        """

        # Initialization of the game fonts
        self.__bigFont = pygame.font.Font('./assets/font/game-font.ttf', size=20)
        self.__midFont = pygame.font.Font('./assets/font/game-font.ttf')
        self.__smallFont = pygame.font.Font('./assets/font/game-font.ttf')

        # Initialization of the game parameters
        self.__currMode = GameMode.MENU
        self.__prevMode = None
        self.__score = 0
        self.__snake = None
        self.__apples = None
        self.__gameMap = None
    
    def getCurrMode(self):
        """
        Getter function of current game mode.
        """
        return self.__currMode

    def setCurrMode(self, mode):
        """
        Setter function of current game mode.

        Args:
            mode (GameMode): constant representing the current game mode.
        """
        # Update mode info
        self.__prevMode = self.__currMode
        self.__currMode = mode
    
    def spawnApples(self):
        """
        Spawns a few apples on the map.
        """
        # Get window info
        width, height = WINDOW_SIZE[0], WINDOW_SIZE[1]

        # Spawn a few apples
        for _ in range(random.randint(1, APPLE_SPAWN_LIMIT)):
            is_generated = False
            # Generate till you find a safe spot
            while not is_generated:
                x = random.randint(0, width // TILE_SIZE)*TILE_SIZE
                y = random.randint(0, height // TILE_SIZE)*TILE_SIZE

                if (self.__gameMap[y // TILE_SIZE + 1][x // TILE_SIZE + 1] == NO_HASH):
                    is_generated = True

            self.__apples.add(Apple(x, y, self.__gameMap))

    def resetGame(self):
        """
        Resets the game
        """
        # Get window info
        width, height = WINDOW_SIZE[0], WINDOW_SIZE[1]
   
        # Full reset of the game parameters.
        self.__score = 0

        # Set up game map
        n_cols, n_rows = (width // TILE_SIZE) + 2, (height // TILE_SIZE) + 2
        self.__gameMap = []
        
        for _ in range(n_rows):
            arr = []
            for _ in range(n_cols): arr.append(NO_HASH)
            self.__gameMap.append(arr)

        # Mark forbidden fields
        for i in range(n_cols): self.__gameMap[0][i] = self.__gameMap[n_rows-1][i] = OBSTACLE_HASH
        for i in range(n_rows): self.__gameMap[i][0] = self.__gameMap[i][n_cols-1] = OBSTACLE_HASH

        # Prepare sprites before the game
        self.__snake = Snake(self.__gameMap)
        self.__apples = pygame.sprite.Group()
        self.spawnApples()

    def drawBackground(self, screen: pygame.surface.Surface):
        """
        Draws background like chess board.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        """

        width, height = WINDOW_SIZE[0], WINDOW_SIZE[1]
        isLight = True

        # Draw chess board
        for j in range(height // TILE_SIZE):
            isLight = (j % 2 == 0)  # reset at the start of each row
            for i in range(width // TILE_SIZE):
                color = pygame.Color(2, 40, 105) if isLight else pygame.Color(2, 61, 163)
                pygame.draw.rect(screen, color, (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                isLight = not isLight


    def menu(self, screen: pygame.surface.Surface):
        """
        It shows menu on the screen and handles its events.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        """
        # Get window info
        width, height = WINDOW_SIZE[0], WINDOW_SIZE[1]
        self.resetGame()
        
        # Wait till user chooses something
        for event in pygame.event.get():
            # User closes the window
            if event.type == pygame.QUIT:
                self.setCurrMode(GameMode.EXIT)
                return
                
            # User provides us input
            elif event.type == pygame.KEYDOWN:
                    # Runs AI mode
                if event.key == pygame.K_0:
                    self.setCurrMode(GameMode.GAME_AI)
                    return
                    
                # Runs Player mode  
                elif event.key == pygame.K_SPACE:
                    self.setCurrMode(GameMode.GAME_PLAYER)
                    return

        # Render GUI
        self.drawBackground(screen)
            
        # Create text labels
        title = self.__bigFont.render("Choose Game Mode", True, 'white')
        player_option = self.__midFont.render("Press SPACE to Play as Player", True, 'white')
        ai_option = self.__midFont.render("Press 0 to Train AI", True, 'white')
        menu_img = pygame.image.load('./assets/image/snake-menu.png')
        menu_img = pygame.transform.scale(menu_img, MENU_IMG_SIZE)

        # Complete rendering
        screen.blit(menu_img, (width // 2 - menu_img.get_width() // 2, 50))
        screen.blit(title, (width // 2 - title.get_width() // 2, 350))
        screen.blit(player_option, (width // 2 - player_option.get_width() // 2, 450))
        screen.blit(ai_option, (width // 2 - ai_option.get_width() // 2, 520))
        
    def run(self, screen: pygame.surface.Surface):
        """
        It handles input and keeps game playing.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        """
        # Get window size
        width, height = WINDOW_SIZE[0], WINDOW_SIZE[1]

        # Handle user input
        for event in pygame.event.get():
            # Window is closed
            if event.type == pygame.QUIT:
                self.setCurrMode(GameMode.EXIT)
                return

            # Handle user input                
            elif event.type == pygame.KEYDOWN:
                # User forces snake to go up
                if event.key == pygame.K_UP and self.__currMode == GameMode.GAME_PLAYER:
                    self.__snake.set_direction(SnakeDirection.UP)
                
                # User forces snake to go down
                elif event.key == pygame.K_DOWN and self.__currMode == GameMode.GAME_PLAYER:
                    self.__snake.set_direction(SnakeDirection.DOWN)
                
                # User forces snake to go left
                elif event.key == pygame.K_LEFT and self.__currMode == GameMode.GAME_PLAYER:
                    self.__snake.set_direction(SnakeDirection.LEFT)
                
                # User forces snake to go right
                elif event.key == pygame.K_RIGHT and self.__currMode == GameMode.GAME_PLAYER:
                    self.__snake.set_direction(SnakeDirection.RIGHT)
            
                # User wants to pasue the game
                elif event.key == pygame.K_ESCAPE:
                    # Pause the game until user chooses something
                    while True:
                
                        # Handle user input
                        for event in pygame.event.get():
                            # Window is closed
                            if event.type == pygame.QUIT:
                                self.setCurrMode(GameMode.EXIT)
                                return
                            
                            # Go back to menu (ENTER)
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                self.setCurrMode(GameMode.MENU)
                                return
                            
                            # Go back to game (ESC)
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                return
                        
                        # Render GUI
                        pasue_title = self.__bigFont.render('Game Pause', True, 'white')
                        back_to_game_option = self.__midFont.render('Press ESCAPE to go back to the game', True, 'white')
                        back_to_menu_option = self.__midFont.render('Press ENTER to go back to the menu', True, 'white')

                        screen.blit(pasue_title, (width // 2 - pasue_title.get_width() // 2, 150))
                        screen.blit(back_to_game_option, (width // 2 - back_to_game_option.get_width() // 2, 250))
                        screen.blit(back_to_menu_option, (width // 2 - back_to_menu_option.get_width() // 2, 300))
                        pygame.display.flip()

        # Force snake to move
        self.__snake.move()

        # Handle snake events
        snakeEvent = self.__snake.handleEvents(self.__apples, WINDOW_SIZE)

        # Update score and spawn apples
        if (snakeEvent == SnakeEvent.SCORE_UPDATE):
            self.spawnApples()
            self.__score += 100

        # Game over
        elif (snakeEvent == SnakeEvent.GAME_OVER):
            # Pause the game until user chooses something
            if (self.getCurrMode() == GameMode.GAME_PLAYER):
                # Render GUI
                gameover_title = self.__bigFont.render('Game over', True, 'white')
                score_surf = self.__midFont.render(f'Your score is {self.__score}', True, 'white')
                back_to_menu_option = self.__midFont.render('Press SPACE to go back to the menu', True, 'white')

                screen.blit(gameover_title, (width // 2 - gameover_title.get_width() // 2, 150))
                screen.blit(score_surf, (width // 2 - score_surf.get_width() // 2, 225))
                screen.blit(back_to_menu_option, (width // 2 - back_to_menu_option.get_width() // 2, 275))
                pygame.display.flip()
            
                while True:
                    # Handle user input
                    for event in pygame.event.get():
                        # Window is closed
                        if event.type == pygame.QUIT:
                            self.setCurrMode(GameMode.EXIT)
                            return
                                
                        # Go back to menu (SPACE)
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            self.setCurrMode(GameMode.MENU)
                            return
            else:            
                # Logic for AI training
                """
                ... RESTART GAME
                """
                self.resetGame()


        # Create score label
        score_surf = self.__bigFont.render(f"Score: {self.__score}", True, 'white')

        # Render gameplay
        self.drawBackground(screen)
        self.__apples.draw(screen)
        self.__snake.draw(screen)
        screen.blit(score_surf, (width - (score_surf.get_width() + width // 10), 50))
