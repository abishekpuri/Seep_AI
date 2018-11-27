from Classes import Card, Pile, Deck, Player, Center, Ai
import os
import copy
import time
from random import choice
# # Encode the game state from the perspective of a player
# def encodeHistory(player,center):
#     # There is a 52-D vector, 0 if that card is not in hand, 1 if that card is in hand
#     cards = [0 for i in range(52)]
#     for card in player.hand:
#         cards[13*card.suit + card.value - 1] = 1
#     # There is a 13-D vector representing the spades, 0 if that card has not been seen, 1 

def run_game(Center, Player1, Player2,move,debug=False):
    if debug:
        print(Center)
    center = copy.deepcopy(Center)
    p1 = copy.deepcopy(Player1)
    p2 = copy.deepcopy(Player2)
    p1.doMove(move,center)
    if debug:
        print("Player 1 Does",p1.printMove(move))
    while len(p1.hand) > 0 or len(p1.hand) > 0:
        p2.possibleMoves(center)
        p2move = choice(p2.moves)
        if debug:
            print("Player 2 Does",p2.printMove(p2move))
        p2.doMove(p2move,center)
        p1.possibleMoves(center)
        p1move = choice(p1.moves)
        if debug:
            print("Player 1 Does",p2.printMove(p1move))
        p1.doMove(p1move,center)
    if debug:
        print("p1 Score",p1.calculateScore(),"p2 score",p2.calculateScore())
    if p1.calculateScore() > p2.calculateScore():
        return 1
    else:
        return 0

def get_opt_Move(Center,Player1,Player2):
    Player1.possibleMoves(Center)
    maxTime = 5/len(Player1.moves)
    scores = {}
    for move in Player1.moves:
        score = 0
        count = 0
        currTime = time.time()
        while time.time() - currTime < maxTime:
            count += 1
            score += run_game(Center,Player1,Player2,move)
        scores[Player1.printMove(move)] = (move,float(score/count))
    move = scores[max(scores.keys(), key=(lambda k: scores[k][1]))][0]
    print("Opt Move",Player1.printMove(move))
    Player1.doMove(move,Center)
    return move
def playGame():
    gameHistory = []
    center = Center.Center()
    deck = Deck.Deck()
    computer = Player.Player(0)
    human = Player.Player(1)

    validBidHand = False
    while not(validBidHand):
        deck = Deck.Deck()
        computer = Player.Player(0)
        human = Player.Player(1)
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
        center.addNewPile(Pile.Pile(card.value,[card]),True)
    human.seeStartingConfiguration(center)
    computer.seeStartingConfiguration(center)

    print(center)
    move = human.HumanChooseMove(center,True,bidValue)
    computer.evaluateOpponentMove(move)
    # os.system('clear')
    for i in range(8):
        human.addCardsToHand([deck.dealCard()])
        computer.addCardsToHand([deck.dealCard()])
    # print("COMPUTERS HAND")
    # print("Computer Hand",computer.hand)
    move = computer.makeMove(center)
    human.evaluateOpponentMove(move)
    while len(computer.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(human.hand)
        move = human.HumanChooseMove(center,False)
        computer.evaluateOpponentMove(move)
        # os.system('clear')
        #move = computer.makeMove(center)
        move = get_opt_Move(center,computer,human)
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
        # os.system('clear')
        #move = computer.makeMove(center)
        move = get_opt_Move(center,computer,human)
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

if __name__ == "__main__":  
    start_time = time.time()
    playGame()
    print("--- %s seconds ---" % (time.time() - start_time))