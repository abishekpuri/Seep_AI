import operator
import random
import copy
from . import Pile


class Player: 
    def __init__(self,id_):
        self.hand = []
        self.cards = []
        self.cardHistory = [[0 for i in range(14)] for j in range(4)]
        self.knownOpponentCards = []
        self.id = id_
        self.seeps = 0
        self.score = 0
    def __eq__(self,other):
        if self.hand == other.hand and self.score == other.score:
            return True
        return False
    def __str__(self):
        return "Players Score is " + str(self.score) + " and his hand is " + str(self.hand)
    def __repr__(self):
        return str(self)
    def seeStartingConfiguration(self,center):
        # For each pile in the center, we add that card to our cardhistory
        for pile in center.piles:
            for card in pile.cards:
                self.cardHistory[card.suit][card.value - 1] = 1
    def addCardsToHand(self,cards):
        for card in cards:
            self.cardHistory[card.suit][card.value - 1] = 1
        self.hand += cards
        self.hand = sorted(self.hand,key=operator.attrgetter('value','suit'))
    def evaluateOpponentMove(self,move):
        # We add the card  played to our card history, and then depending on the move we update our known Opponent Cards
        self.cardHistory[move['card'].suit][move['card'].value - 1] = 1
    def calculateScore(self):
        self.score = 50*self.seeps
        # print("CARDS BEING SCORED",self.cards)
        for card in self.cards:
            if card.suit == 0:
                self.score += card.value
            elif card.value == 1:
                self.score += 1
            elif card.value == 10 and card.suit == 3:
                self.score += 6
        return self.score
    def playCard(self,card_):
        cardToDelete = -1
        for key,card in enumerate(self.hand):
            if card_ == card:
                cardToDelete = key
                break
        if cardToDelete == -1:
            print("Cant Find Card",card_)
        else:
            del self.hand[key]
            print("Played Card",card_)
    def printMove(self,move):
        # Throw
        if move['Type'] == 1:
            return "Throw " + str(move['card']) + " To Center"
        # Create new house
        elif move['Type'] == 2:
            totalValue = sum([p.value for p in move['piles']]) + move['card'].value
            pileValues = [str(p.value) for p in move['piles']]
            return "Combine " + str(move['card']) + " With Piles " + " , ".join(pileValues) + " To Make " + str(totalValue)
        # Put on top of existing uncemented house
        elif move['Type'] == 3:
            pileValues = [str(p.value) for p in move['piles']]
            return "Put "+str(move['card'])+" On Top Of Piles "+" , ".join(pileValues)
        # Combine cards to make a house + merge with uncemented houses => new fixed(cemented) pile
        elif move['Type'] == 4:
            totalValue = sum([p.value for p in move['piles']]) + move['card'].value
            pileValues = [str(p.value) for p in move['piles']]
            return "Use "+str(move['card'])+" To Merge Piles "+" , ".join(pileValues)+" With an Unfixed Pile of value "+str(totalValue)+" Making a New Fixed Pile"
        # Combine cards to make a house + merge with cemented houses
        elif move['Type'] == 5:
            totalValue = sum([p.value for p in move['piles']]) + move['card'].value
            pileValues = [str(p.value) for p in move['piles']]
            return "Use "+str(move['card'])+" To Add Piles "+" , ".join(pileValues)+" To a Fixed Pile of value "+str(totalValue)
        # Put on top of existing cemented house
        elif move['Type'] == 6:
            return "Put "+str(move['card'])+" On Top Of Fixed Pile "+str(move['piles'][0].value)
        # Pick up
        elif move['Type'] == 7:
            pileValues = [str(p.value) for p in move['piles']]
            return "Use "+str(move['card'])+" To Pick Up Piles "+" , ".join(pileValues)
    def possibleMoves(self,center,bidMove=False,bid=0):
        moves = []
        # Throw Card To Center
        currentPileValues = [i.value for i in center.piles]
        for card in self.hand:
            possiblePickUps = center.getMoves(card.value)
            fixedPiles = list(filter(lambda x: x.fixed,center.piles))
            notFixedPiles = list(filter(lambda x: not(x.fixed),center.piles))

            if card.value not in currentPileValues and card.value not in [sum([p.value for p in q]) for q in possiblePickUps]:
                if not(bidMove) or card.value == bid:
                    moves.append({'Type': 1, 'card': card})

            for points in range(max(9-card.value,0),max(14-card.value,0)):
                if points > 0 and [c.value for c in self.hand].count(card.value + points) >= 1:
                    waysToMake = center.getMoves(points,False)
                    if len(waysToMake) > 0 and (card.value + points) not in currentPileValues and (not(bidMove) or card.value + points == bid):
                        for way in waysToMake:
                            moves.append({'Type':2, 'card': card,'piles':way})

            if card.value >= 9 and [c.value for c in self.hand].count(card.value) >= 2 and (not(bidMove) or bid == card.value):
                waysToMake = center.getMoves(card.value,False)
                for way in waysToMake:
                    moves.append({'Type': 3, 'card': card, 'piles': way})
            
            for points in range(max(9-card.value,0),max(14-card.value,0)):
                if points > 0 and [c.value for c in self.hand].count(card.value + points) >= 1 and (not(bidMove) or card.value + points == bid):
                    waysToMake = center.getMoves(points,False)
                    if len(waysToMake) > 0 and (card.value + points) in [p.value for p in notFixedPiles]:
                        for way in waysToMake:
                            moves.append({'Type':4, 'card': card,'piles':way})

            for points in range(max(9-card.value,0),max(14-card.value,0)):
                if points > 0 and [c.value for c in self.hand].count(card.value + points) >= 1 and not(bidMove):
                    waysToMake = center.getMoves(points,False)
                    if len(waysToMake) > 0 and (card.value + points) in [p.value for p in fixedPiles]:
                        for way in waysToMake:
                            moves.append({'Type':5, 'card': card,'piles':way})

            if [c.value for c in self.hand].count(card.value) >= 2 and not(bidMove):
                for pile in fixedPiles:
                    if pile.value == card.value:
                        moves.append({'Type': 6, 'card':card, 'piles': [pile]})
                        break

            for pickup in possiblePickUps:
                if not(bidMove) or card.value == bid:
                    moves.append({'Type':7, 'card': card, 'piles': pickup})
        moves = sorted(moves,key=lambda x: x['Type'])
        self.moves = moves

    def HumanChooseMove(self,center,bidMove=False,bid=0):
        self.possibleMoves(center,bidMove,bid)
        for key,move in enumerate(self.moves):
            new_center = copy.deepcopy(center)
            self.doMove(move,new_center,True)
            if len(new_center.piles) == 0:
                fitness = 50 + sum([p.score for p in move['piles']])
            elif len(new_center.piles) == 1 or \
               (len(list(filter(lambda x: x.fixed,new_center.piles))) == 0 and sum([p.value for p in new_center.piles]) <= 13):
                fitness = -1
            elif move['Type'] == 7:
                fitness = sum([p.score for p in move['piles']])
            else:
                fitness = 0
            move = self.printMove(move)
            print(key,")",move,"Value:",fitness)
        move = self.moves[int(input("Please Choose a move from above:\n"))]
        self.doMove(move,center)
        return move
    def doMove(self,move,center,test=False):
        if not(test):
            self.hand.pop(self.hand.index(move['card']))
        if move['Type'] == 1:
            center.addNewPile(Pile.Pile(move['card'].value,[move['card']]))
        elif move['Type'] <= 5:
            center.addCardToPiles(move['card'],move['piles'])
        elif move['Type'] == 6:
            center.addCardToPiles(move['card'],move['piles'])
        elif move['Type'] == 7:
            if(not(test)):
                self.cards += center.pickUpPiles(move['card'],move['piles'],self.id)
                if len(center.piles) == 0:
                    self.seeps += 1
            else:
                center.pickUpPiles(move['card'],move['piles'],self.id)
        self.calculateScore()
    def chooseBid(self):
        eligibleCards = list(filter(lambda x: x.value >= 9, self.hand))
        random.shuffle(eligibleCards)
        return eligibleCards.pop().value
    def makeMove(self,center,bidMove=False,bid=0):
        self.possibleMoves(center,bidMove,bid)
        moves = []
        for move in self.moves:
            new_center = copy.deepcopy(center)
            self.doMove(move,new_center,True)
            moves.append((move,self.evaluateMove(move,new_center)))
        moves = sorted(moves,key=lambda x: x[1],reverse=False)
        move = moves.pop()[0]
        print("Computers Move",self.printMove(move))
        self.doMove(move,center)
        return move
        #if(move['Type'] == 7):
            #print("After making move, cards are",self.cards)
    def evaluateMove(self,move,new_center):
        score = 0
        if len(new_center.piles) == 0:
            score = 50 + sum([p.score for p in move['piles']])
        elif len(new_center.piles) == 1 or \
            (len(list(filter(lambda x: x.fixed,new_center.piles))) == 0 and sum([p.value for p in new_center.piles]) <= 13):
            score = -1
        elif move['Type'] == 7:
            score = sum([p.score for p in move['piles']])
        return score
