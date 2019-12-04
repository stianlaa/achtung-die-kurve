import pygame
from common import SNAKE_SIZE, IMAGE_HEAD, SNAKE_SPEED, TURN_SPEED
from math import cos, sin, pi
from util import correctForPositionLoopback, correctForAngleLoopback

class Snake(pygame.sprite.Sprite):
    def __init__(self, owner_id, player, width=SNAKE_SIZE, height=SNAKE_SIZE):
        super(Snake, self).__init__()

        self.owner_id = owner_id
        self.setImage(IMAGE_HEAD[self.owner_id])

    def setImage(self, filename=None):
        if filename is not None:
            self.original_image = pygame.image.load(filename)
            self.original_image = pygame.transform.scale(self.original_image, (SNAKE_SIZE, SNAKE_SIZE))
            self.rect = self.original_image.get_rect()

    def setPos(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def setAng(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def update(self, playerInput):
        moveVector = [SNAKE_SPEED * cos(self.angle * pi / 180), SNAKE_SPEED * sin(self.angle * pi / 180)]

        nextPos = [self.rect.x + moveVector[0], self.rect.y + moveVector[1]]
        nextPos = correctForPositionLoopback(nextPos)
        self.setPos(nextPos)

        nextAngle = self.angle
        if (playerInput is not None):
            if (playerInput == "RIGHT"):
                nextAngle = correctForAngleLoopback(nextAngle - TURN_SPEED)
            elif (playerInput == "LEFT"):
                nextAngle = correctForAngleLoopback(nextAngle + TURN_SPEED)
            self.setAng(nextAngle)
