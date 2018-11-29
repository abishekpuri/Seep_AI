from Classes import Card, Pile, Deck, Player, Center, Ai, MCTSNN, NeuralNetwork
import os
import copy
import numpy as np
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
    training_state = []
    training_value = []
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
    training_state, training_value = mcts_nn_p2.get_training_set()
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
    s, v = mcts_nn_p1.get_training_set()
    training_state = np.append(training_state, s, axis=0)
    training_value = np.append(training_value, v, axis=0)
    player1.doMove(move, center)
    # player2.evaluateOpponentMove(move)
    while len(player1.hand) > 0:
        # print("HUMANS MOVE IS:")
        # human.makeMove(center)
        print(center)
        print(player1.hand)
        mcts_nn_p2 = MCTSNN.MCTSNN(center, player2, player1, True, nn)
        move = mcts_nn_p2.run_simulation()
        s, v = mcts_nn_p2.get_training_set()
        training_state = np.append(training_state, s, axis=0)
        training_value = np.append(training_value, v, axis=0)
        player2.doMove(move,center)
        # os.system('clear')
        # move = computer.makeMove(center)
        mcts_nn_p1 = MCTSNN.MCTSNN(center, player1, player2, True, nn)
        move = mcts_nn_p1.run_simulation()
        s, v = mcts_nn_p1.get_training_set()
        training_state = np.append(training_state, s, axis=0)
        training_value = np.append(training_value, v, axis=0)
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
        s, v = mcts_nn_p2.get_training_set()
        training_state = np.append(training_state, s, axis=0)
        training_value = np.append(training_value, v, axis=0)
        player2.doMove(move, center)
        # os.system('clear')
        # move = computer.makeMove(center)
        mcts_nn_p1 = MCTSNN.MCTSNN(center, player1, player2, False, nn)
        move = mcts_nn_p1.run_simulation()
        s, v = mcts_nn_p1.get_training_set()
        training_state = np.append(training_state, s, axis=0)
        training_value = np.append(training_value, v, axis=0)

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

    return training_state, training_value


if __name__ == "__main__":
    nn = NeuralNetwork.NeuralNetwork()
    times = []
    for i in range(2000):
        start_time = time.time()
        training_state, training_value = playGame(nn)
        nn.train_network(training_state, training_value)
        # print("--- %s seconds ---" % (time.time() - start_time))
        times.append(time.time() - start_time)
    with open('/results/time_taken.txt', 'w') as f:
        for i in range(len(times)):
            string = 'Time for match {} ==> {}'.format(i, times[i])
            f.write(string)

