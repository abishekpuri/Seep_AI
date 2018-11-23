import operator
import random
import copy
from . import Pile
from . import Player


class ZeroAi(Player.Player):
    def __init__(self, id_, opponent=None):
        super().__init__(id_)
        self.opponent = opponent

    def addOpponent(self, opponent):
        self.opponent = opponent

    def makeMove(self, center, bidMove=False, bid=0):
        return

