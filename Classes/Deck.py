import random
from . import Card

class Deck: 
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for value in range(1,14):
                self.cards.append(Card.Card(suit,value))
        random.shuffle(self.cards)
    def dealCard(self):
        return self.cards.pop()