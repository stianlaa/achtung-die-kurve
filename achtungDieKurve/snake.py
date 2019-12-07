import pygame
from common import SNAKE_SIZE, IMAGE_HEAD, IMAGE_BODY, SNAKE_SPEED, TURN_SPEED
from math import cos, sin, pi
from util import correctForPositionLoopback, correctForAngleLoopback
import time

class TailNode(pygame.sprite.Sprite):
    def __init__(self, x, y, image = None, angle = None, width = SNAKE_SIZE, height = SNAKE_SIZE):
        super(TailNode, self).__init__()
        if image == None:
            self.image = pygame.Surface((width, height))
            self.image.fill([0, 0, 0])
        else:
            self.original_image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.original_image, (width, height))
            if angle != None:
                self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Snake(pygame.sprite.Sprite):
    def __init__(self, owner_id, player, width=SNAKE_SIZE, height=SNAKE_SIZE):
        super(Snake, self).__init__()

        self.owner_id = owner_id
        self.setImage(IMAGE_HEAD[self.owner_id])

        self.layingTrail = True
        self.currentTrailIndex = 0
        self.tailNodes = []
        self.trailGroup = pygame.sprite.Group()
        self.dead = False
        self.snakeSpeed = SNAKE_SPEED

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

    def updateBodyTrail(self):
        if self.layingTrail and self.currentTrailIndex % 2:
            self.tailNodes.append(TailNode(self.rect.x, self.rect.y, IMAGE_BODY[self.owner_id], self.angle))
            self.trailGroup.add(self.tailNodes[len(self.tailNodes) - 1])
        self.currentTrailIndex += 1

    def update(self, playerInput):
        self.updateBodyTrail()
        x, y = self.rect.center
        moveVector = [self.snakeSpeed * cos(self.angle * pi / 180), self.snakeSpeed * sin(self.angle * pi / 180)]

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

    def isColliding(self, otherGroup):
        if self.layingTrail and pygame.sprite.spritecollide(self, otherGroup, False):
            return True
        return False

    def applyPowerup(self, powerup):
        if (powerup.powerupType == "speedup"):
            self.snakeSpeed = SNAKE_SPEED*2
        elif (powerup.powerupType == "slowdown"):
            self.snakeSpeed = SNAKE_SPEED*0.5
        elif (powerup.powerupType == "notrail"):
            self.layingTrail = False
    
    def clearPowerupEffect(self, powerupType):
        if (powerupType == "slowdown" or powerupType == "speedup"):
            self.snakeSpeed = SNAKE_SPEED
        elif (powerupType == "notrail"):
            self.layingTrail = True
