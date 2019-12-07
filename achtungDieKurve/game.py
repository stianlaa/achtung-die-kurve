import pygame
from common import WIDTH, HEIGHT, POWERUP_DURATION, PLAYERS, IMAGE_BACKGROUND, FPS, CONTROL_MODE, PRINT_FPS, SCORE_LIMIT
from player import Player
from control import Control
from snake import Snake
from powerup import Powerup
from util import findUnoccupiedPosForSnake, placePowerupAtUnoccupiedPos
from random import randrange
import time

playerList = []
snakeList = []
powerupList = []
activePowerups = []
scoreBoard = []
spriteSnakeGroup = pygame.sprite.Group()
spritePowerupGroup = pygame.sprite.Group()
clock = pygame.time.Clock()

def main():
    init()
    startScreen()
    while True:
        gameOver = False
        roundWinner = gameLoop()
        
        playerList[roundWinner.owner_id].incrementScore()
        if playerList[roundWinner.owner_id].score > SCORE_LIMIT:
            gameOver = True
            roundWinner = None
        
        if (gameOver):
            showScoreboard()
        


def init():
    global DISPLAY, GAMECLOCK

    pygame.init()
    GAMECLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

    for index in range(0, PLAYERS):
        playerControl = Control(index, CONTROL_MODE) 
        playerList.append(Player(index, playerControl))

    drawBackground()


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
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    drawPressAnyKeyToContinue()
    GAMECLOCK.tick(FPS)
    pygame.display.update()
    while True:
        if waitForKeyPress():
            return


def gameLoop():
    # TODO: add begin game countdown
    initGame()
    while True:
        roundWinner = updateGame()
        gameRender()
        if (roundWinner is not None): 
            print("Round winner detected, resetting")
            
            resetForNewRound()
            startScreen()
            return roundWinner


def initGame():
    for index in range(0, PLAYERS):
        newSnake = Snake(index, playerList[index])
        newSnake.setPos(findUnoccupiedPosForSnake(snakeList))
        newSnake.setAng(randrange(0, 360))
        snakeList.append(newSnake)

    spriteSnakeGroup.add(snakeList)
    createAndPlacePowerup()
    print("Number of snakes created: " + str(len(snakeList)))


def resetForNewRound():
    # TODO: clear head of snakes also
    spritePowerupGroup.empty()
    spritePowerupGroup.add()
    for snake in snakeList:
        snake.trailGroup.empty()
        snake.trailGroup.add()
    drawBackground()


def drawBackground():
    global gameBackgroundImage, backgroundRect
    gameBackgroundImage = pygame.image.load(IMAGE_BACKGROUND)
    gameBackgroundImage = pygame.transform.scale(gameBackgroundImage, (WIDTH, HEIGHT))
    backgroundRect = gameBackgroundImage.get_rect()


def updateGame():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()

    for snake in snakeList:
        if not (snake.dead):
            controlInput = playerList[snake.owner_id].getControlInput()
            snake.update(controlInput)
            roundWinner = checkForCollisions(snake)
            if (roundWinner is not None): return roundWinner
        
        for powerup in powerupList:
            if (powerup.isColliding(snake)):
                snake.applyPowerup(powerup)
                activePowerups.append([powerup.powerupType, snake, time.time()])
                powerup.kill()
                powerup.remove()
                powerupList.remove(powerup)
        
    for entry in activePowerups:
        if (entry[2] + POWERUP_DURATION < time.time()):
            entry[1].clearPowerupEffect(entry[0])
            activePowerups.remove(entry)

    if (time.time() > Powerup.nextPowerupSpawn):
        createAndPlacePowerup()

    pygame.display.update()
    GAMECLOCK.tick(FPS)
    calculateFps()


def createAndPlacePowerup():
    powerup = placePowerupAtUnoccupiedPos(snakeList)
    powerupList.append(powerup)
    spritePowerupGroup.add(powerup)


def checkForCollisions(snake):
    snakeListCopy = snakeList.copy()
    snakeListCopy.remove(snake)

    if snake.isColliding(snake.trailGroup.sprites()[:-5]):
        roundWinner = killSnake(snake)
        if (roundWinner is not None): return roundWinner

    for otherSnake in snakeListCopy:
        if snake.isColliding(otherSnake.trailGroup):
            playerList[otherSnake.owner_id].score += 1
            roundWinner = killSnake(snake)
            if (roundWinner is not None): return roundWinner


def killSnake(snake):
    snake.dead = True
    return checkForWinConditions()


def checkForWinConditions():
    livingSnakes = 0
    livingSnake = None
    for snake in snakeList:
        if not (snake.dead): 
            livingSnakes += 1
            livingSnake = snake

    if (livingSnakes == 1):
        roundWinner = livingSnake
        return roundWinner


def calculateFps():
    if (PRINT_FPS):
        clock.tick()
        fps = clock.get_fps()
        print("fps: " + str(fps))


def gameRender():
    DISPLAY.blit(gameBackgroundImage, backgroundRect)

    spriteSnakeGroup.draw(DISPLAY)
    spritePowerupGroup.draw(DISPLAY)

    for snake in snakeList:
        snake.trailGroup.draw(DISPLAY)


def showScoreboard():
    print("Scoreboard!")
    for p in playerList:
        print("Player: " + str(p.player_id) + ", score: " + str(p.score))


def quitGame():
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
