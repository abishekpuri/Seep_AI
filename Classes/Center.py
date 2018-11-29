from . import Pile
import operator
import copy
import itertools

# class Center:
#     def __init__(self):
#         self.piles = [] # This is an array of all the piles in the game
#         self.dp = [] # This matrix is used to find the combinations of piles that make up a target
#         self.lastPickUp = -1 # This is the ID of the player who picked up a pile last, for end of game
#     def __str__(self): 
#         str_ = "Center has " + str(len(self.piles)) + " Piles:"
#         for pile in self.piles:
#             str_ += "\n" + str(pile)
#         return str_
#     def addNewPile(self,pile,biddingStage=False): # This function is called whenever a new pile is added to the Center
#         return ""
#     def pickUpPiles(self,card,piles,id_): # This function is called whenever an array of piles are picked up. 
#         return ""
#     def getCombinations(self,target,includeFixed=True): #This function gets all possible pile combinations to make target.
#         return ""
                             


class Center:
    def __init__(self):
        self.piles = []
        self.dp = []
        self.lastPickUp = -1
    def __str__(self):
        str_ = "Center has "+str(len(self.piles)) + " Piles:\n"
        for pile in self.piles:
            str_+= str(pile) + '\n'
        return str_
    def __eq__(self,other):
        return self.piles == other.piles
    def __repr__(self):
        return str(self)
    def pickUpPiles(self,card,piles,id_):
        self.lastPickUp = id_
        if sum([pile.value for pile in piles]) == card.value:
            # We now have to find all other piles that make up this value
            combosRemaining = True
            cards = [card]
            while combosRemaining:
                combos = self.getMoves(card.value)
                if len(combos) == 0:
                    combosRemaining = False
                else:
                    combo = combos[0]
                    for pile in combo:
                        cards += pile.cards
                        self.piles.pop(self.piles.index(pile))
            return cards
        else:
            #print(card,piles)
            raise ValueError("You cannot pick up those piles, value isn't matching")
    def finalCleanUp(self,player):
        for pile in self.piles:
            player.cards += pile.cards
    def addCardToPiles(self,card,piles):
        # Any Pile Fixed?
        if sum([pile.fixed for pile in piles]) == 0:
            # No
            totalValue = sum([pile.value for pile in piles]) + card.value
            # Is the total Value of piles and cards >= 9 and <=13?
            if totalValue <= 13 and totalValue >= 9:
                # Yes
                # Is there another pile with the same total Value?
                if totalValue in [pile.value for pile in self.piles]:
                    matchingPileIndex = [pile.value for pile in self.piles].index(totalValue) 
                    matchingPile = self.piles[matchingPileIndex]
                    # Yes
                    # Is the other pile fixed?
                    if matchingPile.fixed:
                        # Yes
                        self.addUnfixedToFixed(card,piles,matchingPile)
                    else:
                        # No
                        self.mergeUnfixedToFixed(card,piles,matchingPile)
                else:
                    # No
                    self.makeUnfixedPile(card,piles,totalValue)
            else:
                # No
                # Is the sum of all piles >= 9 and sum = card?
                if totalValue - card.value >= 9 and totalValue == card.value * 2:
                    # Yes
                    self.MakeUnfixedIntoFixed(card,piles)
                else:
                    # No
                    #print(card,piles)
                    raise ValueError("Combining Piles and Cards makes a number to big or too small")
        else:
            # Yes
            # Is there only 1 Pile and that Piles value matches the card value?
            if len(piles) == 1 and piles[0].value == card.value:
                #Yes
                self.addCardToFixedPile(card,piles[0])
            else:
                #No
                #print(piles)
                raise ValueError("Given ",len(piles),"Piles. First Pile Value is",piles[0].value," whilst card value",\
                                card.value)
                
    def addUnfixedToFixed(self,card,piles,matchingpileindex):
        #print("adding unfixed to fixed")
        cards = [card]
        for pile in piles:
            cards += pile.cards
            self.piles.pop(self.piles.index(pile))
        matchingpile = Pile.Pile(self.piles[self.piles.index(matchingpileindex)].value,[])
        for pile in self.piles:
            if pile.value == matchingpile.value:
                cards += pile.cards
                self.piles.pop(self.piles.index(pile))
        for card in cards:
            matchingpile.addCard(card,False)
        matchingpile.fixed = True
        self.piles.append(matchingpile)
        self.piles = sorted(self.piles,key=operator.attrgetter('value'))  
    def mergeUnfixedToFixed(self,card,piles,matchingpileindex):  
        #print("merging unfixed with a fixed")
        cards = [card]
        for pile in piles:
            cards += pile.cards
            self.piles.pop(self.piles.index(pile))
        matchingpile = Pile.Pile(self.piles[self.piles.index(matchingpileindex)].value,[])
        for pile in self.piles:
            if pile.value == matchingpile.value:
                cards += pile.cards
                self.piles.pop(self.piles.index(pile))
        for card in cards:
            matchingpile.addCard(card,False)
        matchingpile.fixed = True
        self.piles.append(matchingpile)
        self.piles = sorted(self.piles,key=operator.attrgetter('value'))  
    def makeUnfixedPile(self,card,piles,totalValue): 
        #print("making a new unfixed pile")
        cards = [card]
        for pile in piles:
            cards += pile.cards
            self.piles.pop(self.piles.index(pile))
        newPile = Pile.Pile(totalValue,cards,False)
        self.piles.append(newPile)
        self.piles = sorted(self.piles,key=operator.attrgetter('value'))        
    def MakeUnfixedIntoFixed(self,card,piles):
        #print("turning an unfixed into a fixed")
        cards = [card]
        for pile in piles:
            cards += pile.cards
            self.piles.pop(self.piles.index(pile))
        newPile = Pile.Pile(card.value,cards,True)
        self.piles.append(newPile)
        self.piles = sorted(self.piles,key=operator.attrgetter('value'))        
    def addCardToFixedPile(self,card,p_):
        #print("adding to a fixed pile")
        cards = [card]
        matchingPileIndex = self.piles.index(p_)
        for pile in self.piles:
            if pile.value == self.piles[matchingPileIndex].value and not(pile == p_):
                cards += pile.cards
                self.piles.pop(self.piles.index(pile))
                matchingPileIndex = self.piles.index(p_)
        for c in cards:
            try:
                self.piles[self.piles.index(p_)].addCard(c,False)
            except:
                print("An exception occurred", p_)
        
    def addNewPile(self,pile,bidStage=False):
        for p in self.piles:
            if p.value == pile.value and not(bidStage):
                raise ValueError("You Cannot Add a pile which matches an Existing Pile")
        self.piles.append(pile)
        self.piles = sorted(self.piles,key=operator.attrgetter('value'))
    def deletePile(self,pile):
        pileToDelete = -1
        for key,pile_ in enumerate(self.piles):
            if pile_ == pile:
                pileToDelete = key
                break
        if pileToDelete > -1:
            self.piles.pop(pileToDelete)
    def getMoves(self,target,getFixed=True):
        self.notFixedPiles = list(filter(lambda x: not(x.fixed),self.piles))
        pset = []
        for n in range(len(self.notFixedPiles) + 1):
            for sset in itertools.combinations(self.notFixedPiles, n):
                pset.append(list(sset))
        if getFixed:
            pset += list(map(lambda x: [x],filter(lambda x: x.fixed,self.piles)))
        sols = []
        for sol in pset:
            if sum([s.value for s in sol]) == target:
                sols.append(sol)
        return sols
