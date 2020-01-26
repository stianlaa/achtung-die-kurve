import pygame
from faceControls import faceControlLoop
from threading import Thread, Event

playerKeyboardControls = [
    [pygame.K_RIGHT, pygame.K_LEFT],
    [pygame.K_d, pygame.K_a],
    [pygame.K_n, pygame.K_m],
    [pygame.K_p, pygame.K_o]]

controls = []

def initiateFaceControls():
    t = Thread(target=faceControlLoop, args=(controls,))
    t.start()

class Control():
    def __init__(self, index, controlMode):
        self.player_id = index
        self.controlMode = controlMode
        # TODO: set allowed events to keyboard list

        if (controlMode == "KEYBOARD"):
            keys = playerKeyboardControls[index]
            right = lambda: pygame.key.get_pressed()[keys[0]]
            left = lambda: pygame.key.get_pressed()[keys[1]]
            controls.append({"RIGHT": right, "LEFT": left})
        elif (controlMode == "HANDS"):
            print("Hand gesture control, coming soon, to an achtung near you!")
        elif (controlMode == "FACE"):
            print("Face control chosen")
        else:
            print("Missing control mode")

    def getControlInput(self):
        if (self.controlMode == "KEYBOARD"):
            if (controls[self.player_id]["RIGHT"]()):
                return "RIGHT"
            elif (controls[self.player_id]["LEFT"]()):
                return "LEFT"
            else:
                return None
        elif (self.controlMode == "FACE"):
            if controls is None or len(controls) == 0:
                return None
            else:
                return controls[self.player_id]["turnDirection"]
        else:
            return None