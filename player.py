# from common import *

class Player():
    def __init__(self, index, control):
        self.player_id = index
        self.playerControl = control
        self.score = 0
    
    def getControlInput(self):
        return self.playerControl.getControlInput()

    def incrementScore(self):
        self.score += 1