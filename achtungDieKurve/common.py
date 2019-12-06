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

WIDTH = 1280
HEIGHT = 720
PLAYERS = 4
FPS = 30
SNAKE_SIZE = 10
SNAKE_SPEED = 4
TURN_SPEED = 3
CONTROL_MODE = "KEYBOARD"