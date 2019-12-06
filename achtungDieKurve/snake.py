import pygame
from common import SNAKE_SIZE, IMAGE_HEAD, SNAKE_SPEED, TURN_SPEED
from math import cos, sin, pi
from util import correctForPositionLoopback, correctForAngleLoopback
import time

class Snake(pygame.sprite.Sprite):
    def __init__(self, owner_id, player, width=SNAKE_SIZE, height=SNAKE_SIZE):
        super(Snake, self).__init__()

        self.owner_id = owner_id
        self.setImage(IMAGE_HEAD[self.owner_id])

    def setImage(self, filename=None):
        if filename is not None:
            self.original_image = pygame.image.load(filename)
            self.original_image = pygame.transform.scale(self.original_image, (SNAKE_SIZE, SNAKE_SIZE))
            self.image = self.original_image
            self.rect = self.image.get_rect()

    def setPos(self, position):
        self.rect.center = (position[0], position[1])

    def setAng(self, angle):
        self.angle = angle

    def update(self, playerInput):
        x, y = self.rect.center
        moveVector = [SNAKE_SPEED * cos(self.angle * pi / 180), SNAKE_SPEED * sin(self.angle * pi / 180)]

        nextPos = [x + moveVector[0], y + moveVector[1]]
        nextPos = correctForPositionLoopback(nextPos)

        nextAngle = self.angle
        if (playerInput is not None):
            if (playerInput == "RIGHT"):
                nextAngle = correctForAngleLoopback(nextAngle + TURN_SPEED)
            elif (playerInput == "LEFT"):
                nextAngle = correctForAngleLoopback(nextAngle - TURN_SPEED)
            self.setAng(nextAngle)

        self.image = pygame.transform.rotate(self.original_image, -nextAngle)
        self.rect = self.image.get_rect()
        self.setPos([int(round(nextPos[0])), int(round(nextPos[1]))])
