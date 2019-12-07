import pygame
from common import IMAGE_POWERUP, POWERUP_SIZE
import time
from random import randrange, randint
from common import POWERUP_AVG_SPAWNDELAY

class Powerup(pygame.sprite.Sprite):
    nextPowerupSpawn = None
    powerup_id = 0

    def __init__(self, x, y, powerupType):
        super(Powerup, self).__init__()

        self.setImage(IMAGE_POWERUP[powerupType])
        self.powerupType = powerupType
        self.setPos([x, y])
        
        
    def setImage(self, filename=None):
        if filename is not None:
            self.original_image = pygame.image.load(filename)
            self.original_image = pygame.transform.scale(self.original_image, (POWERUP_SIZE, POWERUP_SIZE))
            self.image = self.original_image
            self.rect = self.image.get_rect()
    
    def setPos(self, position):
        self.rect.center = (position[0], position[1])

    def initializeAfterClearCheck(self):
        self.setNextSpawntime()
        Powerup.powerup_id += 1
        
    def setNextSpawntime(self):
        Powerup.nextPowerupSpawn = time.time() + randrange(POWERUP_AVG_SPAWNDELAY - 1,POWERUP_AVG_SPAWNDELAY + 1)
    
    def isColliding(self, snake):
        snakeGroup = pygame.sprite.GroupSingle(snake)
        if pygame.sprite.spritecollide(self, snakeGroup, False):
            return True
        return False

def chooseRandomPowerupType():
    powerupTypes = list(IMAGE_POWERUP.keys())
    return powerupTypes[randint(0, len(powerupTypes) -1)]