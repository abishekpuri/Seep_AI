from Classes import Card, Pile, Deck, Player, Center, Ai, MCTS
import os
import copy
import time
import pandas as pd
import argparse

# # Encode the game state from the perspective of a player
# def encodeHistory(player,center):
#     # There is a 52-D vector, 0 if that card is not in hand, 1 if that card is in hand
#     cards = [0 for i in range(52)]
#     for card in player.hand:
#         cards[13*card.suit + card.value - 1] = 1
#     # There is a 13-D vector representing the spades, 0 if that card has not been seen, 1 

timeForMCTS = 1000000

def playGame():
    gameHistory = []
    center = Center.Center()
    deck = Deck.Deck()
    human = Ai.Ai(0)
    computer = Player.Player(1)
    human.addOpponent(computer)

    validBidHand = False
    while not(validBidHand):
        deck = Deck.Deck()
        human = Ai.Ai(0)
        computer = Player.Player(1)
        human.addOpponent(computer)
        for i in range(4):
            human.addCardsToHand([deck.dealCard()])
            computer.addCardsToHand([deck.dealCard()])
        if max([c.value for c in human.hand]) >= 9:
            validBidHand = True

    print("Entering the Bidding Stage")
    print("Human Hand")
    print(human.hand)
    # bidValue = int(input("Choose a Bid From Your Hand. -1 To Reshuffle\n"))
    bidValue = human.chooseBid() # random bid
    print("BID VALUE IS",bidValue)
    for i in range(4):
        card = deck.dealCard()
        human.cardHistory[card.suit][card.value - 1] = 1
        computer.cardHistory[card.suit][card.value - 1] = 1
        center.addNewPile(Pile.Pile(card.value,[card]),True)

    print(center)
    move = human.makeMove(center,True,bidValue)
    computer.evaluateOpponentMove(move)
    #human.makeMove(center,True,bidValue)
    for i in range(8):
        human.addCardsToHand([deck.dealCard()])
        computer.addCardsToHand([deck.dealCard()])
    #print("COMPUTERS HAND")
    print(center)
    print("Computer Hand",computer.hand)
    move = MCTS.MCTS(center,computer,human,True,timeForMCTS,roundForMCTS).run_simulation()
    computer.doMove(move,center)
    human.evaluateOpponentMove(move)

    while len(computer.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(human.hand)
        # move = human.HumanChooseMove(center,False)
        move = human.makeMove(center)
        computer.evaluateOpponentMove(move)
        print(center)
        print(computer.hand)
        print("COMPUTERS MOVE IS:")
        # move = computer.makeMove(center)
        move = MCTS.MCTS(center,computer,human,True,timeForMCTS,roundForMCTS).run_simulation()
        computer.doMove(move,center)
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
        # move = human.HumanChooseMove(center,False)
        move = human.makeMove(center)
        computer.evaluateOpponentMove(move)
        print(center)
        print(computer.hand)
        print("COMPUTERS MOVE IS:")
        move = MCTS.MCTS(center,computer,human,False,timeForMCTS,roundForMCTS).run_simulation()
        computer.doMove(move,center)
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
    return (gameHistory, human.calculateScore(), computer.calculateScore())

# playGame()

parser = argparse.ArgumentParser()
parser.add_argument("-d1", help='Depth in expectimax', required=True, type=int)
parser.add_argument("-d2", help='Depth in minimax', required=True, type=int)
parser.add_argument('-l', nargs=4, help='Weights in evaluation function', required=True, type=int)
parser.add_argument("-r", help='Round in MCTS', required=True, type=int)
parser.add_argument("-c", help='Current gameplay', required=True, type=int)
parser.add_argument("-m", help='Maximun gameplay', required=True, type=int)
args = parser.parse_args()
# print(args.d1)
Ai.depth1 = args.d1
Ai.depth2 = args.d2
Ai.weights = args.l
roundForMCTS = args.r
currentGame = args.c
maxGameplay = args.m

resultDir = 'results/'
gameStatDir = 'gameResult/'
scoresFile = 'scores.csv'

if __name__ == "__main__":
    try:
        scoresDf = pd.read_csv(resultDir+scoresFile, index_col=0)
    except pd.io.common.EmptyDataError:
        print("WARMING:",resultDir+scoresFile, "is empty")
        scoresDf = pd.DataFrame(columns=['MCTS', 'Expectiminimax'])
    while currentGame < maxGameplay:
        print('Game', currentGame)
        Ai.scoresHistory = []
        MCTS.winRateHistory = []
        start_time = time.time()
        history, hmScore, aiScore = playGame()
        newScore = pd.Series({'MCTS':hmScore, 'Expectiminimax':aiScore},name=currentGame)
        scoresDf = scoresDf.append(newScore)
        scoresDf.to_csv(resultDir+scoresFile)
        print("--- %s seconds ---" % (time.time() - start_time))
        # print(len(Ai.scoresHistory))
        # print(len(MCTS.winRateHistory))
        gameStat = pd.DataFrame({'Expectiminimax scores':Ai.scoresHistory, 'MCTS win rates':MCTS.winRateHistory})
        gameStat.to_csv(resultDir+gameStatDir+'gameplay'+str(currentGame)+'.csv')
        currentGame+=1
