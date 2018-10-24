class Card:
    def __init__(self,suit,value):
        self.value = value
        self.suit = suit
    def __str__(self):
        suits = ['Spades','Hearts','Clubs','Diamonds']
        return str(self.value) + " Of " + suits[self.suit]
    def __repr__(self):
        return str(self)
    def __eq__(self,other):
        return self.value == other.value and self.suit == other.suit
        