import operator
import random
import copy
from . import Pile
from . import Player


class Ai(Player.Player): 
    def __init__(self,id_, opponent=None):
        super().__init__(id_)
        self.opponent = opponent

    def addOpponent(self,opponent):
        self.opponent = opponent

    def makeMove(self,center,bidMove=False,bid=0):
        agent = copy.deepcopy(self)
        opponent = copy.deepcopy(self.opponent)
        temp_center = copy.deepcopy(center)
        bestMoves = []
        depth = 1

        def minimax(center, agent, opponent, depth, maxAgent):
            agent.possibleMoves(center)
            opponent.possibleMoves(center)
            if depth == 0 or not agent.moves or not opponent.moves:
                return agent.calculateScore() - opponent.calculateScore()

            if maxAgent:
                final_score = float('-inf')
                final_move = None
                for move in agent.moves:
                    new_center = copy.deepcopy(center)
                    new_agent = copy.deepcopy(agent)
                    new_agent.doMove(move,new_center)

                    score = minimax(new_center, new_agent, opponent, depth, False)

                    if score > final_score:
                        final_score = score
                        final_move = move
                return score
            else:
                final_score = float('inf')
                final_move = None
                for move in opponent.moves:
                    new_center = copy.deepcopy(center)
                    new_opponent = copy.deepcopy(opponent)
                    new_opponent.doMove(move,new_center)

                    score = minimax(new_center, agent, new_opponent, depth - 1, True)

                    if score < final_score:
                        final_score = score
                        final_move = move
                return score
        
        scores = []
        self.possibleMoves(temp_center)
        for move in self.moves:
            new_center = copy.deepcopy(temp_center)
            new_agent = copy.deepcopy(agent)
            new_agent.doMove(move,new_center)

            score = minimax(new_center, new_agent, opponent, depth, False)
            scores.append((move, score))

        scores = sorted(scores,key=lambda x: x[1],reverse=True)
        for s in scores:
            print("AI have move %s with score %i" % (self.printMove(s[0]), s[1]))

        print(self.printMove(scores[0][0]))
        self.doMove(scores[0][0], center)