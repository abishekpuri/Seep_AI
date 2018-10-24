class Pile:
    def __init__(self,value,card,fixed=False):
        self.cards = card
        self.score = 0
        self.fixed = fixed
        for card in self.cards:
            if card.suit == 0:
                self.score += card.value
            elif card.value == 1:
                self.score += 1
            elif card.value == 10 and card.suit == 3:
                self.score += 6
        self.value = value
    def __str__(self):
        return ("Fixed " if self.fixed else "Unfixed ") + "Pile Value:" + str(self.value) + \
                ", Score:" + str(self.score) + ", Cards: " + str(self.cards)
    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        return self.cards == other.cards and self.score == other.score \
           and self.value == other.value and self.fixed == other.fixed
    def addCard(self,card,changingValue):
        if changingValue:
            self.value += card.value
        self.cards.append(card)
        if card.suit == 0:
            self.score += card.value
        elif card.value == 1:
            self.score += 1
        elif card.value == 10 and card.suit == 3:
            self.score += 6