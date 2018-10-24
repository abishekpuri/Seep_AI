import unittest
from Classes import Card, Pile, Deck, Player, Center

# class possibleMovesTests(unittest.TestCase):
#     def setUp(self):
#         self.player = Player.Player(0)
#         self.center = Center.Center()
#     def test_pickUp(self):
#         self.player.hand = [Card.Card(0,5)]
#         self.center.piles = [Pile.Pile(5,[]),Pile.Pile(4,[]),Pile.Pile(1,[])]
#         self.player.possibleMoves(self.center)
#         print(self.player.moves)
#         self.center.piles = [Pile.Pile(9,[],True),Pile.Pile(1,[])]
#         self.player.hand = [Card.Card(0,10)]
#         self.player.possibleMoves(self.center)
#         #print(self.player.moves)


#unittest.main(exit=False)

pplayer = Player.Player(0)
pcenter = Center.Center()
pplayer.hand = [Card.Card(0,5)]
pcenter.piles = [Pile.Pile(5,[]),Pile.Pile(4,[]),Pile.Pile(1,[])]
pplayer.possibleMoves(pcenter)
print("MOVES FOR 5",pplayer.moves)
pcenter.piles = [Pile.Pile(9,[],True),Pile.Pile(1,[])]
pplayer.hand = [Card.Card(0,10)]
pplayer.possibleMoves(pcenter)
print("MOVES FOR 10",pplayer.moves)
