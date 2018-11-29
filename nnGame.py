from Classes import Card, Pile, Deck, Player, Center, Ai, MCTSNN, NeuralNetwork
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


def playGame(nn):
    gameHistory = []
    center = Center.Center()
    deck = Deck.Deck()
    player1 = Player.Player(0)
    player2 = Player.Player(1)

    validBidHand = False
    while not (validBidHand):
        deck = Deck.Deck()
        player1 = Player.Player(0)
        player2 = Player.Player(1)
        for i in range(4):
            player2.addCardsToHand([deck.dealCard()])
            player1.addCardsToHand([deck.dealCard()])
        if max([c.value for c in player2.hand]) >= 9:
            validBidHand = True

    print("Entering the Bidding Stage")
    print("Player 2 Hand")
    print(player2.hand)
    # bidValue = int(input("Choose a Bid From Your Hand. -1 To Reshuffle\n"))
    bidValue = player2.chooseBid()
    print("BID VALUE IS", bidValue)
    for i in range(4):
        card = deck.dealCard()
        center.addNewPile(Pile.Pile(card.value, [card]), True)
    player2.seeStartingConfiguration(center)
    player1.seeStartingConfiguration(center)

    print(center)
    mcts_nn_p2 = MCTSNN.MCTSNN(center, player2, player1, True, nn)
    move = mcts_nn_p2.run_simulation(True, bidValue)
    mcts_nn_p2.send_training_set()
    player2.doMove(move,center)
    # player1.evaluateOpponentMove(move)
    # os.system('clear')
    for i in range(8):
        player2.addCardsToHand([deck.dealCard()])
        player1.addCardsToHand([deck.dealCard()])
    # print("COMPUTERS HAND")
    # print("Computer Hand",computer.hand)
    mcts_nn_p1 = MCTSNN.MCTSNN(center, player1, player2, True, nn)
    move = mcts_nn_p1.run_simulation()
    mcts_nn_p1.send_training_set()
    player1.doMove(move, center)
    # player2.evaluateOpponentMove(move)
    while len(player1.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(player1.hand)
        mcts_nn_p2 = MCTSNN.MCTSNN(center, player2, player1, True, nn)
        move = mcts_nn_p2.run_simulation()
        mcts_nn_p2.send_training_set()
        player2.doMove(move,center)
        # os.system('clear')
        # move = computer.makeMove(center)
        mcts_nn_p1 = MCTSNN.MCTSNN(center, player1, player2, True, nn)
        move = mcts_nn_p1.run_simulation()
        mcts_nn_p1.send_training_set()
        player1.doMove(move, center)
    print("HALF WAY SCORES")
    print("Human Score", player2.calculateScore())
    print("Computer Score", player1.calculateScore())

    for i in range(12):
        player2.addCardsToHand([deck.dealCard()])
        player1.addCardsToHand([deck.dealCard()])

    while len(player1.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(player2.hand)
        mcts_nn_p2 = MCTSNN.MCTSNN(center, player2, player1, False, nn)
        move = mcts_nn_p2.run_simulation()
        mcts_nn_p2.send_training_set()
        player2.doMove(move, center)
        # os.system('clear')
        # move = computer.makeMove(center)
        mcts_nn_p1 = MCTSNN.MCTSNN(center, player1, player2, False, nn)
        move = mcts_nn_p1.run_simulation()
        mcts_nn_p1.send_training_set()
        player1.doMove(move, center)
        # player1.evaluateOpponentMove(move)

    # print("FINAL CENTER")
    # print(center)
    print("ALL THE CENTER PILES ARE GOING TO ", center.lastPickUp)
    print("SCORES BEFORE CLEANING UP")
    print("Human Score", player2.calculateScore())
    print("Computer Score", player1.calculateScore())
    center.finalCleanUp(player1 if center.lastPickUp == 0 else player2)
    print("FINAL SCORE")
    print("Human Score", player2.calculateScore())
    print("Computer Score", player1.calculateScore())

    return gameHistory


if __name__ == "__main__":
    nn = NeuralNetwork.NeuralNetwork()
    nn.build_network()
    for i in range(1000):
        start_time = time.time()
        playGame(nn)
        print("--- %s seconds ---" % (time.time() - start_time))
