import pygame
from os import path

SOURCE_FOLDER = path.dirname(path.abspath(__file__))
IMAGE_BACKGROUND = SOURCE_FOLDER + "/img/background.jpg"
WIDTH = 1280
HEIGHT = 720
PLAYERS = 4
FPS = 30

def main():
    init()
    startScreen()
    while True:
        gameLoop()

def init():
    global DISPLAY, GAMECLOCK, gameBackgroundImage, backgroundRect

    pygame.init()
    GAMECLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

    playerList = []
    for index in range(0, PLAYERS):
        playerList.append(Player(index))
    
    gameBackgroundImage = pygame.image.load(IMAGE_BACKGROUND)
    gameBackgroundImage = pygame.transform.scale(gameBackgroundImage, (WIDTH, HEIGHT))
    backgroundRect = gameBackgroundImage.get_rect()

def waitForKeyPress(): 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            else:
                return True
    return False

def drawPressAnyKeyToContinue(): 
    msgFont = pygame.font.Font('freesansbold.ttf', 30)
    msgSurf = msgFont.render('Press any key to continue', True, ( 40,  40,  40)) 
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH /2, HEIGHT - (msgRect.height + 20))
    DISPLAY.blit(msgSurf, msgRect)

class Player():

    def __init__(self, index):
        self.snake_id = -1
        self.player_id = index

def startScreen():
    # surface.blit(source, dest): "Draws a source Surface onto this Surface."
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    drawPressAnyKeyToContinue()
    
    pygame.display.update()
    
    while True:
        if waitForKeyPress():
            return
            
    GAMECLOCK.tick(FPS)

def updateGame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # whats this (events)?
            quitGame()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()

    # Update snake positions
    # and check for powerup spawns
    return "updated game state"

def gameLoop():
    initGame()
    while True:
        gameOver = updateGame()
        gameRender()
        if gameOver:
            return

def initGame():
    # Todo: place snakes, and their initial directions
    print("initializing game resources")

def gameRender():
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    # print("rendering game game resources")
    # draw snake states

def quitGame():
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
