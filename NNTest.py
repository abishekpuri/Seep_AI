from Classes import NeuralNetwork, Player, Center, Card, Pile,MCTS
import numpy as np

def testInput():
    player = Player.Player(0)
    player.hand = [Card.Card(0, 2), Card.Card(1, 4), Card.Card(1, 7),  Card.Card(2, 7), Card.Card(0, 13)]
    player.cards = [Card.Card(3, 1), Card.Card(3, 4), Card.Card(0, 7), Card.Card(2, 13), Card.Card(3, 13)]
    center = Center.Center()
    pile1 = Pile.Pile(12, [Card.Card(0, 3), Card.Card(1, 12), Card.Card(3, 9)])
    pile2 = Pile.Pile(11, [Card.Card(2, 11), Card.Card(0, 4), Card.Card(0, 7)])
    pile3 = Pile.Pile(9, [Card.Card(0, 1), Card.Card(1, 2), Card.Card(0, 6), Card.Card(2, 9)])
    center.piles = [pile1, pile2, pile3]
    nn = NeuralNetwork.NeuralNetwork()
    scoreV, handV, centerV = nn.state2input(player, center)
    player2 = Player.Player(1)
    player2.hand = [Card.Card(0, 5), Card.Card(0, 7), Card.Card(3, 12), Card.Card(3,1)]

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
    player.hand = [Card.Card(0, 2), Card.Card(1, 4), Card.Card(1, 7), Card.Card(2, 7), Card.Card(0, 13)]
    player.cards = [Card.Card(3, 1), Card.Card(3, 4), Card.Card(0, 7), Card.Card(2, 13), Card.Card(3, 13)]

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
    _input = nn.state2input(player, opp, center)
    print(_input)

    '''
    # generate batches for training
    sarray = np.expand_dims(_score, axis=0)
    sarray = np.append(sarray, np.expand_dims(_score, axis=0), axis=0)
    sarray = np.append(sarray, np.expand_dims(_score, axis=0), axis=0)
    print(sarray.shape)
    print(sarray)
    charray = np.expand_dims(_ch, axis=0)
    charray = np.stack((charray, _ch), axis=0)
    '''

    batch = np.expand_dims(_input, axis=0)
    batch = np.append(batch, np.expand_dims(_input, axis=0), axis=0)

    out = np.array([0.5, 0.2])
    print(out.shape)
    # build & train
    nn.buildNetwork()
    nn.train_network(batch, out)
    nn.show_model_summary()
    #nn.load_checkpoint()

    # predict the value of a state
    print(nn.predict(player, opp, center))

test()