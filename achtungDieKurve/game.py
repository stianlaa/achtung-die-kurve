import pygame
from common import *
from player import *
from snake import *

playerList = []
snakeList = []

def main():
    init()
    startScreen()
    while True:
        gameLoop()

####################################### PREPARE FOR GAME

def init():
    global DISPLAY, GAMECLOCK, gameBackgroundImage, backgroundRect

    pygame.init()
    GAMECLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

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

def startScreen():
    # surface.blit(source, dest): "Draws a source Surface onto this Surface."
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    drawPressAnyKeyToContinue()
    
    pygame.display.update()
    
    while True:
        if waitForKeyPress():
            return
            
    GAMECLOCK.tick(FPS)

####################################### RUN GAME

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
    # TODO: create snake objects
    for index in range(0, PLAYERS):
        snakeList.append(Snake(index, playerList[index]))
    # TODO: place snakes, and their initial directions

    # TODO: draw snake tails
    print("initializing game resources")

def gameRender():
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    # print("rendering game game resources")
    # draw snake states

####################################### SUMMARIZE GAME AND OFFER RESTART

def quitGame():
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
