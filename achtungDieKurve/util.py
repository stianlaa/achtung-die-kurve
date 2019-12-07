from common import HEIGHT, WIDTH
import random
from math import sqrt
from powerup import Powerup, chooseRandomPowerupType

MINIMUM_DISTANCE = 30


def distance(xA, yA, xB, yB):
    return sqrt((xB - xA)**2 + (yB - yA)**2)


def findUnoccupiedPosForSnake(snakeList):
    posUndetermined = True
    while posUndetermined:
        candidateX = random.randint(MINIMUM_DISTANCE, WIDTH - MINIMUM_DISTANCE)
        candidateY = random.randint(MINIMUM_DISTANCE, HEIGHT - MINIMUM_DISTANCE)

        if (len(snakeList) == 0):
            return [candidateX, candidateY]

        if (all(distance(snake.rect.x, snake.rect.y, candidateX, candidateY) >= MINIMUM_DISTANCE for snake in snakeList)):
            return [candidateX, candidateY]


def placePowerupAtUnoccupiedPos(snakeList):
    posUndetermined = True
    while posUndetermined:
        candidateX = random.randint(MINIMUM_DISTANCE, WIDTH - MINIMUM_DISTANCE)
        candidateY = random.randint(MINIMUM_DISTANCE, HEIGHT - MINIMUM_DISTANCE)

        if (all(distance(snake.rect.x, snake.rect.y, candidateX, candidateY) >= MINIMUM_DISTANCE for snake in snakeList)):
            candidatePowerup = Powerup(candidateX, candidateY, chooseRandomPowerupType())
            
            if all(not candidatePowerup.isColliding(snake.trailGroup) for snake in snakeList):
                candidatePowerup.initializeAfterClearCheck()
                return candidatePowerup


def correctForPositionLoopback(position):
    correctedPosition = position
    if position[0] < 0:
        correctedPosition[0] = WIDTH + position[0]
    elif position[0] > WIDTH:
        correctedPosition[0] = position[0] - WIDTH

    if position[1] < 0:
        correctedPosition[1] = HEIGHT + position[1]
    elif position[1] > HEIGHT:
        correctedPosition[1] = position[1] - HEIGHT

    return correctedPosition


def correctForAngleLoopback(angle):
    if angle >= 360:
        return angle - 360
    elif angle <= 0:
        return angle + 360
    return angle
