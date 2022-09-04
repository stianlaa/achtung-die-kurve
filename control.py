import pygame

playerKeyboardControls = [
    [pygame.K_RIGHT, pygame.K_LEFT],
    [pygame.K_d, pygame.K_a],
    [pygame.K_n, pygame.K_m],
    [pygame.K_p, pygame.K_o]]

controls = []

class Control():
    def __init__(self, index, controlMode):
        self.player_id = index
        # TODO: set allowed events to keyboard list

        if (controlMode == "KEYBOARD"):
            keys = playerKeyboardControls[index]
            right = lambda: pygame.key.get_pressed()[keys[0]]
            left = lambda: pygame.key.get_pressed()[keys[1]]
            controls.append({"RIGHT": right, "LEFT": left})
        elif (controlMode == "HANDS"):
            print("Hand gesture control, coming soon, to an achtung near you!")
        elif (controlMode == "FACE"):
            print("Face control, coming soon, to an achtung near you!")
        else:
            print("Missing control mode")

    def getControlInput(self):
        if (controls[self.player_id]["RIGHT"]()):
            return "RIGHT"
        elif (controls[self.player_id]["LEFT"]()):
            return "LEFT"
        else:
            return None