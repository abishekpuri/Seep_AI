from Classes import NeuralNetwork, Player, Center, Card, Pile
import numpy as np

def testInput():
    player = Player.Player(0)
    player.hand = [Card.Card(0, 2), Card.Card(1, 4), Card.Card(1, 7), Card.Card(0, 13)]
    player.cards = [Card.Card(3, 1), Card.Card(3, 4), Card.Card(0, 7), Card.Card(2, 13)]
    center = Center.Center()
    pile1 = Pile.Pile(12, [Card.Card(0, 3), Card.Card(1, 12), Card.Card(3, 9)])
    pile2 = Pile.Pile(11, [Card.Card(2, 11), Card.Card(0, 4), Card.Card(0, 7)])
    pile3 = Pile.Pile(9, [Card.Card(0, 1), Card.Card(1, 2), Card.Card(0, 6), Card.Card(2, 9)])
    center.piles = [pile1, pile2, pile3]
    nn = NeuralNetwork.NeuralNetwork()
    scoreV, handV, centerV = nn.stateToInput(player, center)

    print(player)
    print(center)

    print("Score vector")
    print(scoreV)
    print("="*10)
    print("Hand vector")
    print(handV)
    print("=" * 10)
    print("Center vector")
    print(centerV)
    print("=" * 10)
    return scoreV, handV, centerV

def test():
    # me
    player = Player.Player(0)
    player.hand = [Card.Card(0, 2), Card.Card(1, 4), Card.Card(1, 7), Card.Card(0, 13)]
    player.cards = [Card.Card(3, 1), Card.Card(3, 4), Card.Card(0, 7), Card.Card(2, 13)]

    # opp
    opp = Player.Player(1)
    opp.hand = [Card.Card(0, 2), Card.Card(1, 4), Card.Card(1, 7), Card.Card(0, 13)]
    opp.cards = [Card.Card(2, 11), Card.Card(0, 9), Card.Card(2, 1), Card.Card(1, 1)]

    center = Center.Center()
    pile1 = Pile.Pile(12, [Card.Card(0, 3), Card.Card(1, 12), Card.Card(3, 9)])
    pile2 = Pile.Pile(11, [Card.Card(2, 11), Card.Card(0, 4), Card.Card(0, 7)])
    pile3 = Pile.Pile(9, [Card.Card(0, 1), Card.Card(1, 2), Card.Card(0, 6), Card.Card(2, 9)])
    center.piles = [pile1, pile2, pile3]
    nn = NeuralNetwork.NeuralNetwork()
    _score, _hand, _center = nn.stateToInput(player, opp, center)

    # generate batches for training
    sarray = np.stack((_score, _score), axis=0)
    harray = np.stack((_hand, _hand), axis=0)
    carray = np.stack((_center, _center), axis=0)
    out = np.array([1, 1])

    # build & train
    nn.buildNetwork()
    nn.trainNetwork(sarray, harray, carray, out)
    nn.showModelSummary()
    # nn.loadCheckpoint()

    # predict the value of a state
    nn.predict(player, opp, center)

test()