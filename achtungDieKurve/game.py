import pygame
from common import WIDTH, HEIGHT, POWERUP_DURATION, PLAYERS, IMAGE_BACKGROUND, FPS, CONTROL_MODE, PRINT_FPS, SCORE_LIMIT, PLACEMENT
from player import Player
from control import Control, initiateFaceControls
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
            while True:
                if waitForKeyPress():
                    return
        

def init():
    global DISPLAY, GAMECLOCK

    pygame.init()
    GAMECLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

    initiateFaceControls()

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
    pygame.display.update()


def drawCountdown(count):
    drawBackground()
    DISPLAY.blit(gameBackgroundImage, backgroundRect)

    msgFont = pygame.font.Font('freesansbold.ttf', 60)
    msgSurf = msgFont.render(str(count), True, (40, 40, 40))
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH / 2, HEIGHT*0.6)
    DISPLAY.blit(msgSurf, msgRect)
    pygame.display.update()


def startScreen():
    DISPLAY.blit(gameBackgroundImage, backgroundRect)
    drawPressAnyKeyToContinue()
    GAMECLOCK.tick(FPS)
    
    while True:
        if waitForKeyPress():
            for i in range(3, 0, -1):
                drawCountdown(i)
                time.sleep(1)
            return


def gameLoop():
    initGame()
    while True:
        roundWinner = updateGame()
        gameRender()
        if (roundWinner is not None): 
            print("Round winner detected, resetting")
            
            resetForNewRound()
            # TODO: check for global wincondition
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
    spritePowerupGroup.empty()
    spritePowerupGroup.add()
    spriteSnakeGroup.empty()
    spriteSnakeGroup.add()
    for snake in snakeList:
        snake.trailGroup.empty()
        snake.trailGroup.add()
    drawBackground()
    snakeList.clear()
    powerupList.clear()
    activePowerups.clear()


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

    spritePowerupGroup.draw(DISPLAY)
    
    for snake in snakeList:
        snake.trailGroup.draw(DISPLAY)

    spriteSnakeGroup.draw(DISPLAY)

def drawPlayerscoreOnScreen(player, placement):
    print("Writing entry for player " + str(player.player_id) + " placement: " + str(placement))
    msgFont = pygame.font.Font('freesansbold.ttf', 40 - placement*5)
    msgSurf = msgFont.render("{}  Player {}   total score:  {}".format(PLACEMENT[placement], str(player.player_id + 1), str(player.score)), True, (40, 40, 40))
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH / 2, HEIGHT*(0.8 - placement*0.2))
    DISPLAY.blit(msgSurf, msgRect)

def showScoreboard():
    # TODO: fix countdown showing up before scoreboard
    playerListByScore = sorted(playerList, key= lambda p: p.score, reverse=True)

    for placement, player in enumerate(playerListByScore):
        drawPlayerscoreOnScreen(player, placement)
        
    pygame.display.update()


def quitGame():
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
