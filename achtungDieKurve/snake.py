import pygame
from common import SNAKE_SIZE, IMAGE_HEAD

class Snake(pygame.sprite.Sprite):
    def __init__(self, owner_id, player, width=SNAKE_SIZE, height=SNAKE_SIZE):
        super(Snake, self).__init__()

        self.owner_id = owner_id
        self.setImage(IMAGE_HEAD[self.owner_id])

    def setImage(self, filename=None):
        if filename is not None:
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, (SNAKE_SIZE, SNAKE_SIZE))
            self.rect = self.image.get_rect()

    def setPos(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def setAng(self, angle):
        self.angle = angle
