import pygame
from common import WIDTH, HEIGHT, PLAYERS, IMAGE_BACKGROUND, FPS
from player import Player
from snake import Snake
from util import findUnoccupiedPos
from random import randrange
import time

playerList = []
snakeList = []
spriteSnakeGroup = pygame.sprite.Group()


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
    msgSurf = msgFont.render('Press any key to continue', True, (40, 40, 40))
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH / 2, HEIGHT - (msgRect.height + 20))
    DISPLAY.blit(msgSurf, msgRect)


def startScreen():
    # surface.blit(source, dest): "Draws a source Surface onto this Surface."
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    drawPressAnyKeyToContinue()
    GAMECLOCK.tick(FPS)
    pygame.display.update()
    while True:
        if waitForKeyPress():
            return


def gameLoop():
    initGame()
    while True:
        gameOver = updateGame()
        gameRender()
        if gameOver:
            return


def initGame():
    for index in range(0, PLAYERS):
        newSnake = Snake(index, playerList[index])
        newSnake.setPos(findUnoccupiedPos(snakeList))
        newSnake.setAng(randrange(0, 360))
        snakeList.append(newSnake)

    spriteSnakeGroup.add(snakeList)

    print("Number of snakes created: " + str(len(snakeList)))
    # TODO: draw snake tails
    # TODO: draw snake bodies


def updateGame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()

    # TODO: Update snakes
    for snake in snakeList:
        snake.update("RIGHT")

    # TODO: check for powerup spawns
    # TODO: check for wincondition
    pygame.display.update()
    GAMECLOCK.tick(FPS)
    return False


def gameRender():
    DISPLAY.blit(gameBackgroundImage, backgroundRect)

    # Draw heads
    spriteSnakeGroup.draw(DISPLAY)
    # draw snake states

def quitGame():
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
