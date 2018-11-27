from Classes import Player, Center, Card, Pile,MCTS
import copy

def run_test():
    player = Player.Player(0)
    player.hand = [Card.Card(0, 2), Card.Card(1, 4), Card.Card(1, 7), Card.Card(0, 13),Card.Card(1,6),Card.Card(2,5),Card.Card(1,12)]
    player2 = Player.Player(1)
    player2.hand = [Card.Card(0, 5), Card.Card(0, 7), Card.Card(3, 12), Card.Card(3,1),Card.Card(2,4),Card.Card(3,8),Card.Card(2,9)]

    center = Center.Center()
    pile1 = Pile.Pile(12, [Card.Card(0, 3), Card.Card(1, 12), Card.Card(3, 9)])
    pile2 = Pile.Pile(11, [Card.Card(2, 11), Card.Card(0, 4), Card.Card(0, 7)])
    pile3 = Pile.Pile(9, [Card.Card(0, 1), Card.Card(1, 2), Card.Card(0, 6), Card.Card(2, 9)])
    center.piles = [pile1, pile2, pile3]

    simul = MCTS.MCTS(center,player,player2)
    simul.run_simulation()
    player.possibleMoves(center)

    return simul

