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

PLACEMENT = {0: "WINNER",
             1: "2nd",
             2: "3rd",
             3: "4th"}

PLAYER_COLORS = [
    (0, 203, 181),
    (191, 30, 46),
    (252, 165, 68),
    (186, 218, 85)]

WIDTH = 1280
# For øyeblikket er cameraoutput 0.75 i screen ratio
# for å bruke facecontrol burde disse ha ratio 0.75
HEIGHT = 960

PLAYERS = 4
SCORE_LIMIT = 8

FPS = 30
PRINT_FPS = False

SNAKE_SIZE = 12
SNAKE_SPEED = 4
TURN_SPEED = 5
TRAILSKIP_AVG_DELAY = 6
TRAILSKIP_LENGTH = 0.5

POWERUP_DURATION = 2
POWERUP_AVG_SPAWNDELAY = 10
POWERUP_SIZE = 15

CONTROL_MODE = "KEYBOARD"