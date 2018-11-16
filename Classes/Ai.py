import operator
import random
import copy
from . import Pile
from . import Player


class Ai(Player.Player): 
    def __init__(self,id_):
        super().__init__(id_)
        self.opponents = []
    def addOpponent(self,opponent):
        self.opponents.append(opponent)
    def makeMove(self,center,bidMove=False,bid=0):
        self.possibleMoves(center,bidMove,bid)
        moves = []
        for move in self.moves:
            new_center = copy.deepcopy(center)
            self.doMove(move,new_center,True)
            if len(new_center.piles) == 0:
                moves.append((move,50 + sum([p.score for p in move['piles']])))
            elif len(new_center.piles) == 1 or \
               (len(list(filter(lambda x: x.fixed,new_center.piles))) == 0 and sum([p.value for p in new_center.piles]) <= 13):
                moves.append((move,-1))
            elif move['Type'] == 7:
                moves.append((move,sum([p.score for p in move['piles']])))
            else:
                moves.append((move,0))
        moves = sorted(moves,key=lambda x: x[1],reverse=False)
        move = moves.pop()[0]
        print(self.printMove(move))
        self.hand.pop(self.hand.index(move['card']))
        self.doMove(move,center)
        if(move['Type'] == 7):
            print("After making move, cards are",self.cards)