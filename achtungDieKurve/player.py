# from common import *

class Player():
    def __init__(self, index, control):
        self.player_id = index
        self.playerControl = control
    
    def getControlInput(self):
        return self.playerControl.getControlInput()