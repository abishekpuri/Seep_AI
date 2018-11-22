import operator
import random
import copy
from . import Pile
from . import Player
from . import Card

def evaluateState(state, agent):
    score = agent.calculateScore() - state[1]
    # if len(center.piles) == 1 or (len(list(filter(lambda x: x.fixed,center.piles))) == 0 and sum([p.value for p in center.piles]) <= 13):
    #     score -= 50 # prediction of leaving only 1 pile in the center
    return score, 0

def convertArrayToCards(array):
    cards = []
    for suit in range(4):
        for value in range(1,14):
            if not array[suit][value-1]: # Card not seen
                cards.append(Card.Card(suit,value))
    return cards

def calculateScore(cards, seeps):
    score = 50*seeps
    # print("CARDS BEING SCORED",self.cards)
    for card in cards:
        if card.suit == 0:
            score += card.value
        elif card.value == 1:
            score += 1
        elif card.value == 10 and card.suit == 3:
            score += 6
    return score

def doMove(move,center,id,test=False):
    cards = []
    seeps = 0
    if move['Type'] == 1:
        center.addNewPile(Pile.Pile(move['card'].value,[move['card']]))
    elif move['Type'] <= 5:
        center.addCardToPiles(move['card'],move['piles'])
    elif move['Type'] == 6:
        center.addCardToPiles(move['card'],move['pile'])
    elif move['Type'] == 7:
        if(not(test)):
            cards += center.pickUpPiles(move['card'],move['piles'],id)
            if len(center.piles) == 0:
                seeps += 1
        else:
            center.pickUpPiles(move['card'],move['piles'],id)
    return cards, seeps

def possibleMovesOfCards(center,cardsArray,bidMove=False,bid=0):
    moves = []
    # Throw Card To Center
    currentPileValues = [i.value for i in center.piles]
    cards = convertArrayToCards(cardsArray)
    for card in cards:
        possiblePickUps = center.getMoves(card.value)
        fixedPiles = list(filter(lambda x: x.fixed,center.piles))
        notFixedPiles = list(filter(lambda x: not(x.fixed),center.piles))

        if card.value not in currentPileValues and card.value not in [sum([p.value for p in q]) for q in possiblePickUps]:
            if not(bidMove) or card.value == bid:
                moves.append({'Type': 1, 'card': card})

        for points in range(max(9-card.value,0),max(14-card.value,0)):
            if points > 0 and [c.value for c in cards].count(card.value + points) >= 1:
                waysToMake = center.getMoves(points,False)
                if len(waysToMake) > 0 and (card.value + points) not in currentPileValues and (not(bidMove) or card.value + points == bid):
                    for way in waysToMake:
                        moves.append({'Type':2, 'card': card,'piles':way})

        if card.value >= 9 and [c.value for c in cards].count(card.value) >= 2 and (not(bidMove) or bid == card.value):
            waysToMake = center.getMoves(card.value,False)
            for way in waysToMake:
                moves.append({'Type': 3, 'card': card, 'piles': way})
        
        for points in range(max(9-card.value,0),max(14-card.value,0)):
            if points > 0 and [c.value for c in cards].count(card.value + points) >= 1 and (not(bidMove) or card.value + points == bid):
                waysToMake = center.getMoves(points,False)
                if len(waysToMake) > 0 and (card.value + points) in [p.value for p in notFixedPiles]:
                    for way in waysToMake:
                        moves.append({'Type':4, 'card': card,'piles':way})

        for points in range(max(9-card.value,0),max(14-card.value,0)):
            if points > 0 and [c.value for c in cards].count(card.value + points) >= 1 and not(bidMove):
                waysToMake = center.getMoves(points,False)
                if len(waysToMake) > 0 and (card.value + points) in [p.value for p in fixedPiles]:
                    for way in waysToMake:
                        moves.append({'Type':5, 'card': card,'piles':way})

        if [c.value for c in cards].count(card.value) >= 2 and not(bidMove):
            for pile in fixedPiles:
                if pile.value == card.value:
                    moves.append({'Type': 6, 'card':card, 'pile': [pile]})
                    break

        for pickup in possiblePickUps:
            if not(bidMove) or card.value == bid:
                moves.append({'Type':7, 'card': card, 'piles': pickup})
    moves = sorted(moves,key=lambda x: x['Type'])
    return moves

def minimax(state, agent, depth, maxAgent, alpha, beta):
    center, opponentScore = state
    agent.possibleMoves(center)
    opponentMoves = possibleMovesOfCards(center, agent.cardHistory)
    # print(opponentMoves)
    pass
    if depth == 0 or not agent.moves:
        return evaluateState(state, agent)

    if maxAgent:
        final_score = float('-inf')
        final_move = None
        for move in agent.moves:
            new_center = copy.deepcopy(center)
            new_agent = copy.deepcopy(agent)
            new_agent.doMove(move,new_center)
            new_state = (new_center, opponentScore)
            score,_ = minimax(new_state, new_agent, depth, False, alpha, beta)
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
        for move in opponentMoves:
            new_center = copy.deepcopy(center)
            oppoCards, oppoSeep = doMove(move,new_center,1) # Hardcode id to 1, means human
            new_state = (new_center, opponentScore+calculateScore(oppoCards, oppoSeep)) # Update score as well
            score,_ = minimax(new_state, agent, depth - 1, True, alpha, beta)
            
            if score < final_score:
                final_score = score
                final_move = move
            if score < alpha:
                return score, final_move
            beta = min(beta, score)
        #print("Final Move is",final_move)
        return score, final_move

class Ai(Player.Player): 
    def __init__(self,id_, opponent=None):
        super().__init__(id_)
        self.opponent = opponent

    def addOpponent(self,opponent):
        self.opponent = opponent

    def makeMove(self,center,bidMove=False,bid=0):
        agent = copy.deepcopy(self)
        temp_center = copy.deepcopy(center)
        depth = 1
        #print("Current Agent Score Is",agent.calculateScore())
        opponentScore = self.opponent.calculateScore()
        
        alpha=float('-inf')
        beta=float('inf')
        scores = []
        self.possibleMoves(temp_center)
        for move in self.moves:
            new_center = copy.deepcopy(temp_center)
            new_agent = copy.deepcopy(agent)
            new_agent.doMove(move,new_center)
            #print("move is",move)

            state = (new_center, opponentScore)
            score,_ = minimax(state, new_agent, depth, False, alpha, beta)
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