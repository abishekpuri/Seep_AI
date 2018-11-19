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
        numOfAgents = len(self.opponents)+1
        alpha = float('-inf')
        beta = float('inf')
        agents = [self] + self.opponents
        depth = 1
        bestMoves = []

        def alphaBeta(center, depth, agents, agentIndex, alpha, beta, bestMoves, bidMove=False, bid=0):
          agent = agents[agentIndex]

          # Collect legal moves and successor states
          agent.possibleMoves(center,bidMove,bid)

          if depth == 0 or len(agent.moves) == 0:
            return agent.calculateScore() - agents[1].calculateScore()

          if agentIndex == 0: # maximize the value
            value = float("-inf")
            bestmove = None
            for move in agent.moves:
            #   print(agent.printMove(move))
              new_center = copy.deepcopy(center)
              new_agent = copy.deepcopy(agent)
              new_agent.doMove(move,new_center)
              agents[agentIndex] = new_agent
              v = alphaBeta(new_center, depth, agents, agentIndex + 1, alpha, beta, bestMoves)
              if v > value:
                value = v
                bestmove = move
            #   if value > beta:
            #     bestMoves.append(bestmove)
            #     return value
            #   alpha = max(alpha, value)
            bestMoves.append(bestmove)
            return value
          else: # minimize the value
            value = float("inf")
            for move in agent.moves:
            #   print(agent.printMove(move))
              new_center = copy.deepcopy(center)
              new_agent = copy.deepcopy(agent)
              new_agent.doMove(move,new_center)
              agents[agentIndex] = new_agent
              if agentIndex + 1 == numOfAgents:
                v = alphaBeta(new_center, depth - 1, agents, 0, alpha, beta, bestMoves)
                if v < value:
                    value = v
                    bestmove = move
              else:
                v = alphaBeta(new_center, depth, agents, agentIndex + 1, alpha, beta, bestMoves)
                if v < value:
                    value = v
                    bestmove = move
            #   if value < alpha:
            #     bestMoves.append(bestmove)
            #     return value
            #   beta = min(beta, value)
            bestMoves.append(bestmove)
            return value

        # Collect legal moves and successor states
        self.possibleMoves(center,bidMove,bid)

        # Choose one of the best actions
        scores = []
        agent = copy.deepcopy(self)
        for i, move in enumerate(self.moves):
          bestMoves = []
          print("AI Move is %s " % self.printMove(move))
          new_center = copy.deepcopy(center)
          agent.doMove(move,new_center)
          new_agent = copy.deepcopy(agent)
          agents[0] = new_agent
          score = alphaBeta(new_center, depth, agents, 1, alpha, beta, bestMoves)
          print("Best moves are %s" % bestMoves)
          print("Score is %i" % score)
          scores.append(score)
          if score > beta:
            break
          alpha = max(alpha, score)
        print("Scores For Moves",scores)
        print(self.moves)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        move = self.moves[chosenIndex]
        print(self.printMove(move))
        self.hand.pop(self.hand.index(move['card']))
        self.doMove(move,center)
