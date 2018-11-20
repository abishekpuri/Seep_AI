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
        depth = 2
        #print("Current Agent Score Is",agent.calculateScore())
        def minimax(center, agent, opponent, depth, maxAgent, alpha, beta):
            agent.possibleMoves(center)
            opponent.possibleMoves(center)
            if depth == 0 or not agent.moves or not opponent.moves:
                return agent.calculateScore() - opponent.calculateScore(),0

            if maxAgent:
                final_score = float('-inf')
                final_move = None
                for move in agent.moves:
                    new_center = copy.deepcopy(center)
                    new_agent = copy.deepcopy(agent)
                    new_agent.doMove(move,new_center)
                    score,_ = minimax(new_center, new_agent, opponent, depth, False, alpha, beta)
                    if score > final_score:
                        final_score = score
                        final_move = move
                    if score > beta:
                        return score,final_move
                    alpha = max(alpha, score)
                return score,final_move
            else:
                final_score = float('inf')
                final_move = None
                for move in opponent.moves:
                    new_center = copy.deepcopy(center)
                    new_opponent = copy.deepcopy(opponent)
                    new_opponent.doMove(move,new_center)
                    score,_ = minimax(new_center, agent, new_opponent, depth - 1, True, alpha, beta)
                    
                    if score < final_score:
                        final_score = score
                        final_move = move
                    if score < alpha:
                        return score, final_move
                    beta = min(beta, score)
                #print("Final Move is",final_move)
                return score, final_move
        
        alpha=float('-inf')
        beta=float('inf')
        scores = []
        self.possibleMoves(temp_center)
        for move in self.moves:
            new_center = copy.deepcopy(temp_center)
            new_agent = copy.deepcopy(agent)
            new_agent.doMove(move,new_center)
            #print("move is",move)
            score,_ = minimax(new_center, new_agent, opponent, depth, False, alpha, beta)
            #print("Final Agent Score is",new_agent.calculateScore(),"Final Opponent Score is",-(score - new_agent.calculateScore()))
            scores.append((move, score,_))
            if score > beta:
                break
            alpha = max(alpha, score)

        scores = sorted(scores,key=lambda x: x[1],reverse=True)
        # for s in scores:
        #     #print("AI have move %s with score %i" % (self.#printMove(s[0]), s[1]))
        print(self.printMove(scores[0][0]))
        print("Opponents Best Move",self.printMove(scores[0][2]))
        #print(self.printMove(scores[0][0]))
        self.doMove(scores[0][0], center)
        return scores[0][0]