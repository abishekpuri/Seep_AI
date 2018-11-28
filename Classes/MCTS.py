from random import choice
import copy
import time
import math
class MCTS():
    def __init__(self,Center,Player1,Player2,firstRound):
        self.center = Center
        self.player = Player1
        self.opponent = Player2 
        self.wins = {}
        self.plays = {}
        self.best_move = -1
        self.firstRound = firstRound
    def next_state(self,Center,Player1,move):
        center = copy.deepcopy(Center)
        p1 = copy.deepcopy(Player1)
        p1.doMove(move,center)
        return (str(p1),str(center))
    def run_game(self,debug=False):
        plays,wins = self.plays,self.wins
        visited_states = set()
        center = copy.deepcopy(self.center)
        p1 = copy.deepcopy(self.player)
        p2 = copy.deepcopy(self.opponent)
        expand = True
        while len(p1.hand) > 0 or len(p1.hand) > 0:
            p1.possibleMoves(center)
            if len(p1.moves) == 0:
                break
            next_states = {str(move):self.next_state(center,p1,move) for move in p1.moves}
            if all(plays.get(next_states[str(move)]) for move in p1.moves):
                log_total = sum(plays[next_states[str(move)]] for move in p1.moves)
                values = [(wins[next_states[str(move)]] / plays[next_states[str(move)]] +
                     1.4 * math.sqrt(log_total / plays[next_states[str(move)]]),move) for move in p1.moves]
                p1move = max(values,key=lambda x: x[0])[1]
            else:
                p1move = choice(p1.moves)
            p1.doMove(p1move,center)
            if expand and (str(p1),str(center)) not in plays:
                expand = False
                plays[(str(p1),str(center))] = 0
                wins[(str(p1),str(center))] = 0
            visited_states.add((str(p1),str(center)))
            p2.possibleMoves(center)
            if len(p2.moves) == 0:
                break
            p2move = choice(p2.moves)
            p2.doMove(p2move,center)
        if not self.firstRound:  
            center.finalCleanUp(p1 if center.lastPickUp == p1.id else p2)
        win = 1 if p1.calculateScore() > p2.calculateScore() else 0
        for p1,center in visited_states:
            if ((str(p1),str(center))) in plays:
                plays[(str(p1),str(center))] += 1
                wins[(str(p1),str(center))] += win
    
    def run_simulation(self):
        games = 0
        currTime = time.time()
        while time.time() - currTime < 10:
            self.run_game()
            games += 1
        print("Total Games",games)
        self.player.possibleMoves(self.center)
        curr_max = -1
        curr_move = 0
        for move in self.player.moves:
            new_center = copy.deepcopy(self.center)
            new_player = copy.deepcopy(self.player)
            new_player.doMove(move,new_center)
            if self.wins[(str(new_player),str(new_center))]/self.plays[(str(new_player),str(new_center))] > curr_max:
                curr_max = self.wins[(str(new_player),str(new_center))]/self.plays[(str(new_player),str(new_center))]
                curr_move = move
        print("Move",curr_move,"Is the best option, with win rate",curr_max)
        return curr_move
