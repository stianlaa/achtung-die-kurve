from common import HEIGHT, WIDTH
import random
from math import sqrt

MINIMUM_DISTANCE = 30


def distance(xA, yA, xB, yB):
    return sqrt((xB - xA)**2 + (yB - yA)**2)


def findUnoccupiedPos(snakeList):
    posUndetermined = True
    while posUndetermined:
        candidateX = random.randint(MINIMUM_DISTANCE, WIDTH - MINIMUM_DISTANCE)
        candidateY = random.randint(MINIMUM_DISTANCE, HEIGHT - MINIMUM_DISTANCE)

        if (len(snakeList) == 0):
            return [candidateX, candidateY]

        if (all(distance(snake.rect.x, snake.rect.y, candidateX, candidateY) >= MINIMUM_DISTANCE for snake in snakeList)):
            return [candidateX, candidateY]
