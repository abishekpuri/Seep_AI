from Classes import Card, Pile, Deck, Player, Center, Ai
import os
import copy
import time
# # Encode the game state from the perspective of a player
# def encodeHistory(player,center):
#     # There is a 52-D vector, 0 if that card is not in hand, 1 if that card is in hand
#     cards = [0 for i in range(52)]
#     for card in player.hand:
#         cards[13*card.suit + card.value - 1] = 1
#     # There is a 13-D vector representing the spades, 0 if that card has not been seen, 1 

def playGame():
    gameHistory = []
    center = Center.Center()
    deck = Deck.Deck()
    computer = Ai.Ai(0)
    human = Player.Player(1)

    computer.addOpponent(human)

    validBidHand = False
    while not(validBidHand):
        deck = Deck.Deck()
        computer = Ai.Ai(0)
        human = Player.Player(1)
        computer.addOpponent(human)
        for i in range(4):
            human.addCardsToHand([deck.dealCard()])
            computer.addCardsToHand([deck.dealCard()])
        if max([c.value for c in human.hand]) >= 9:
            validBidHand = True

    print("Entering the Bidding Stage")
    print("Human Hand")
    print(human.hand)
    bidValue = int(input("Choose a Bid From Your Hand. -1 To Reshuffle\n"))
    #bidValue = human.chooseBid()
    print("BID VALUE IS",bidValue)
    for i in range(4):
        card = deck.dealCard()
        human.cardHistory[card.suit][card.value - 1] = 1
        computer.cardHistory[card.suit][card.value - 1] = 1
        center.addNewPile(Pile.Pile(card.value,[card]),True)

    print(center)
    move = human.HumanChooseMove(center,True,bidValue)
    computer.evaluateOpponentMove(move)
    #human.makeMove(center,True,bidValue)
    for i in range(8):
        human.addCardsToHand([deck.dealCard()])
        computer.addCardsToHand([deck.dealCard()])
    #print("COMPUTERS HAND")
    print(center)
    print("Computer Hand",computer.hand)
    move = computer.makeMove(center)
    human.evaluateOpponentMove(move)

    while len(computer.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(human.hand)
        move = human.HumanChooseMove(center,False)
        computer.evaluateOpponentMove(move)
        print(computer.hand)
        print("COMPUTERS MOVE IS:")
        move = computer.makeMove(center)
        human.evaluateOpponentMove(move)

    print("HALF WAY SCORES")
    print("Human Score",human.calculateScore())
    print("Computer Score",computer.calculateScore())

    for i in range(12):
        human.addCardsToHand([deck.dealCard()])
        computer.addCardsToHand([deck.dealCard()])

    while len(computer.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(human.hand)
        move = human.HumanChooseMove(center,False)
        computer.evaluateOpponentMove(move)
        print("COMPUTERS MOVE IS:")
        move = computer.makeMove(center)
        human.evaluateOpponentMove(move)

    
    # print("FINAL CENTER")
    # print(center)
    print("ALL THE CENTER PILES ARE GOING TO ",center.lastPickUp)
    print("SCORES BEFORE CLEANING UP")
    print("Human Score",human.calculateScore())
    print("Computer Score",computer.calculateScore())
    center.finalCleanUp(computer if center.lastPickUp == 0 else human)
    print("FINAL SCORE")
    print("Human Score",human.calculateScore())
    print("Computer Score",computer.calculateScore())
    return gameHistory

playGame()
if __name__ == "__main__":  
    start_time = time.time()
    history = playGame()
    print("--- %s seconds ---" % (time.time() - start_time))