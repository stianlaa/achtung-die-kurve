from os import path

SOURCE_FOLDER = path.dirname(path.abspath(__file__))
IMAGE_BACKGROUND = SOURCE_FOLDER + "/img/background.jpg"
IMAGE_BODY = [SOURCE_FOLDER + "/img/body1.png",
            SOURCE_FOLDER + "/img/body2.png",
            SOURCE_FOLDER + "/img/body3.png",
            SOURCE_FOLDER + "/img/body4.png"]
IMAGE_HEAD = [SOURCE_FOLDER + "/img/head1.png", 
            SOURCE_FOLDER + "/img/head2.png",
            SOURCE_FOLDER + "/img/head3.png",
            SOURCE_FOLDER + "/img/head4.png"]

IMAGE_POWERUP = {"notrail": SOURCE_FOLDER + "/img/powerup_notrail.png",
                "slowdown": SOURCE_FOLDER + "/img/powerup_slowdown.png",
                "speedup": SOURCE_FOLDER + "/img/powerup_speedup.png"}

WIDTH = 1280
HEIGHT = 720

PLAYERS = 2

FPS = 30

SNAKE_SIZE = 10
SNAKE_SPEED = 4
TURN_SPEED = 3

POWERUP_DURATION = 2
POWERUP_AVG_SPAWNDELAY = 10
POWERUP_SIZE = 15

CONTROL_MODE = "KEYBOARD"