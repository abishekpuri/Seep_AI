from Classes import Card, Pile, Deck, Player, Center, Ai, MCTS, NeuralNetwork
import os
import copy
import time
# import pandas as pd
import argparse

# # Encode the game state from the perspective of a player
# def encodeHistory(player,center):
#     # There is a 52-D vector, 0 if that card is not in hand, 1 if that card is in hand
#     cards = [0 for i in range(52)]
#     for card in player.hand:
#         cards[13*card.suit + card.value - 1] = 1
#     # There is a 13-D vector representing the spades, 0 if that card has not been seen, 1 

timeForMCTS = 1000000

def playGame(agent, nn):
    humanScoreHistory = []
    computerScoreHistory = []
    gameHistory = []
    center = Center.Center()
    deck = Deck.Deck()
    human = Player.Player(1)
    if agent=='mcts':
        computer = Player.Player(0)
    elif agent=='emm':
        computer = Ai.Ai(0)
        computer.addOpponent(human)
    elif agent=='nn':
        computer = Player.Player(0)

    validBidHand = False
    while not(validBidHand):
        deck = Deck.Deck()
        human = Player.Player(1)
        if agent=='mcts':
            computer = Player.Player(0)
        elif agent=='emm':
            computer = Ai.Ai(0)
            computer.addOpponent(human)
        elif agent=='nn':
            computer = Player.Player(0)
        
        for i in range(4):
            human.addCardsToHand([deck.dealCard()])
            computer.addCardsToHand([deck.dealCard()])
        if max([c.value for c in human.hand]) >= 9:
            validBidHand = True

    print("Entering the Bidding Stage")
    print("Human Hand")
    print(human.hand)
    bidValue = int(input("Choose a Bid From Your Hand. -1 To Reshuffle\n"))
    # bidValue = human.chooseBid() # random bid
    print("BID VALUE IS",bidValue)
    for i in range(4):
        card = deck.dealCard()
        human.cardHistory[card.suit][card.value - 1] = 1
        computer.cardHistory[card.suit][card.value - 1] = 1
        center.addNewPile(Pile.Pile(card.value,[card]),True)

    print("COMPUTERS HAND")
    print(center)
    move = human.HumanChooseMove(center,True,bidValue)
    humanScoreHistory.append(human.calculateScore())
    computer.evaluateOpponentMove(move)
    #human.makeMove(center,True,bidValue)
    for i in range(8):
        human.addCardsToHand([deck.dealCard()])
        computer.addCardsToHand([deck.dealCard()])
    print("COMPUTERS HAND")
    print(center)
    # print("Computer Hand",computer.hand)
    if agent=='mcts':
        move = MCTS.MCTS(center,computer,human,True,timeForMCTS,roundForMCTS).run_simulation()
        computer.doMove(move,center)
    elif agent=='emm':
        move = computer.makeMove(center)
    elif agent=='nn':
        if len(computer.hand) == 1 and len(computer.moves) == 1:
            computer.doMove(computer.moves[0], center)
        else:
            mcts_nn_p1 = MCTSNN.MCTSNN(center, computer, human, True, nn)
            move = mcts_nn_p1.run_simulation()
            computer.doMove(move, center)
    computerScoreHistory.append(computer.calculateScore())
    human.evaluateOpponentMove(move)

    while len(computer.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(human.hand)
        move = human.HumanChooseMove(center,False)
        # move = human.makeMove(center)
        humanScoreHistory.append(human.calculateScore())
        computer.evaluateOpponentMove(move)
        print(center)
        # print(computer.hand)
        print("COMPUTERS MOVE IS:")
        if agent=='mcts':
            move = MCTS.MCTS(center,computer,human,True,timeForMCTS,roundForMCTS).run_simulation()
            computer.doMove(move,center)
        elif agent=='emm':
            move = computer.makeMove(center)
        elif agent=='nn':
            if len(computer.hand) == 1 and len(computer.moves) == 1:
                computer.doMove(computer.moves[0], center)
            else:
                mcts_nn_p1 = MCTSNN.MCTSNN(center, computer, human, True, nn)
                move = mcts_nn_p1.run_simulation()
                computer.doMove(move, center)
        computerScoreHistory.append(computer.calculateScore())
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
        # move = human.makeMove(center)
        humanScoreHistory.append(human.calculateScore())
        computer.evaluateOpponentMove(move)
        print(center)
        print(computer.hand)
        print("COMPUTERS MOVE IS:")
        if agent=='mcts':
            move = MCTS.MCTS(center,computer,human,False,timeForMCTS,roundForMCTS).run_simulation()
            computer.doMove(move,center)
        elif agent=='emm':
            move = computer.makeMove(center)
        elif agent=='nn':
            if len(computer.hand) == 1 and len(computer.moves) == 1:
                computer.doMove(computer.moves[0], center)
            else:
                mcts_nn_p1 = MCTSNN.MCTSNN(center, computer, human, False, nn)
                move = mcts_nn_p1.run_simulation()
                computer.doMove(move, center)
        computerScoreHistory.append(computer.calculateScore())
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
    return (gameHistory, human.calculateScore(), computer.calculateScore(), humanScoreHistory, computerScoreHistory)

# playGame()

parser = argparse.ArgumentParser()
parser.add_argument("type", help='Type of agent', type=str, choices=['mcts', 'emm', 'nn'])
parser.add_argument("-d1", help='Depth in expectimax', type=int)
parser.add_argument("-d2", help='Depth in minimax', type=int)
parser.add_argument('-l', nargs=4, help='Weights in evaluation function', type=int)
parser.add_argument("-r", help='Round in MCTS',  type=int)
# parser.add_argument("-c", help='Current gameplay', required=True, type=int)
# parser.add_argument("-m", help='Maximun gameplay', required=True, type=int)
# parser.add_argument("-d", help='Results directory', required=True, type=str)
args = parser.parse_args()
# print(args.d1)
agentType = args.type
Ai.depth1 = args.d1
Ai.depth2 = args.d2
Ai.weights = args.l
roundForMCTS = args.r

if agentType == 'mcts' and not roundForMCTS:
    parser.error('MCTS need parameter -r for the number of simulation per move')
elif agentType == 'emm' and not args.d1 and not args.d2 and not args.l:
    parser.error('Expectiminimax need parameter -d1, -d2 for the depth of expectimax and minimax and -l for the evaluation weights')

if __name__ == "__main__":
    Ai.scoresHistory = []
    MCTS.winRateHistory = []
    nn = NeuralNetwork.NeuralNetwork()
    start_time = time.time()
    history, hmScore, aiScore, hmScoreHis, aiScoreHis = playGame(agentType, nn)
    print("--- %s seconds ---" % (time.time() - start_time))
