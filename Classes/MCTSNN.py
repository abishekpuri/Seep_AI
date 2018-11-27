from Classes import NeuralNetwork
from random import choice
import copy
import time
import math
import numpy as np

class MCTSNN():
    def __init__(self,Center,Player1,Player2,firstRound, nn):
        self.center = Center
        self.player = Player1
        self.opponent = Player2 
        self.wins = {}
        self.plays = {}
        self.best_move = -1
        self.firstRound = firstRound
        self.nn = nn
        self.visited_states = []
        self.visited_set = set()

    def next_state(self,Center,Player1,move):
        center = copy.deepcopy(Center)
        p1 = copy.deepcopy(Player1)
        p1.doMove(move,center)
        return (str(p1), str(center))

    def _next_state(self,Center,Player1,move):
        center = copy.deepcopy(Center)
        p1 = copy.deepcopy(Player1)
        p1.doMove(move, center)
        return p1, center

    def predictions_from_nn(self, center, player, opponent):
        predictions = []
        for move in player.moves:
            new_player, new_center = self._next_state(center, player, move)
            value = self.nn.predict(new_player, opponent, new_center)[0][0]
            predictions.append((value, move))
        #print("Predictions from nn")
        #print(predictions)
        return predictions

    def run_game(self, bidMove=False, bid=0, debug=False):
        plays, wins = self.plays, self.wins
        visited_states = set()
        center = copy.deepcopy(self.center)
        p1 = copy.deepcopy(self.player)
        p2 = copy.deepcopy(self.opponent)
        expand = True
        while len(p1.hand) > 0 or len(p1.hand) > 0:
            # generate all possible moves
            p1.possibleMoves(center, bidMove, bid)
            # if no moves, break
            if len(p1.moves) == 0:
                break
            # generate next states of possible moves
            next_states = {str(move): self.next_state(center, p1, move) for move in p1.moves}
            if all(plays.get(next_states[str(move)]) for move in p1.moves):
                log_total = sum(plays[next_states[str(move)]] for move in p1.moves)
                values = [(wins[next_states[str(move)]] / plays[next_states[str(move)]] +
                     1.4 * math.sqrt(log_total / plays[next_states[str(move)]]), move) for move in p1.moves]
                p1move = max(values, key=lambda x: x[0])[1]
            else:
                values = self.predictions_from_nn(center, p1, p2)
                p1move = max(values, key=lambda x: x[0])[1]
            p1.doMove(p1move, center)
            if expand and (str(p1), str(center)) not in plays:
                expand = False
                plays[(str(p1), str(center))] = 0
                wins[(str(p1), str(center))] = 0
            if (str(p1), str(center)) not in self.visited_set:
                self.visited_states.append({'player': copy.deepcopy(p1), 'opponent': copy.deepcopy(p2), 'center': copy.deepcopy(center)})
                self.visited_set.add((str(p1), str(center)))
            visited_states.add((str(p1), str(center)))
            p2.possibleMoves(center)
            if len(p2.moves) == 0:
                break
            p2move = choice(p2.moves)
            p2.doMove(p2move, center)
        if not self.firstRound:
            center.finalCleanUp(p1 if center.lastPickUp == p1.id else p2)
        win = 1 if p1.calculateScore() > p2.calculateScore() else 0
        for p1, center in visited_states:
            if (str(p1), str(center)) in plays:
                plays[(str(p1), str(center))] += 1
                wins[(str(p1), str(center))] += win

    def run_simulation(self, bidMove=False, bid=0):
        games = 0
        currTime = time.time()
        while time.time() - currTime < 60:
            self.run_game(bidMove, bid)
            games += 1
        print("Total Games", games)
        self.player.possibleMoves(self.center)
        curr_max = -1
        curr_move = 0
        win_rate = -1
        for move in self.player.moves:
            new_center = copy.deepcopy(self.center)
            new_player = copy.deepcopy(self.player)
            new_player.doMove(move, new_center)
            if (str(new_player), str(new_center)) in self.plays:
                win_rate = self.wins[(str(new_player), str(new_center))]/self.plays[(str(new_player), str(new_center))]
                print('{} with win rate {}'.format(str(new_player), win_rate))
            if win_rate > curr_max:
                curr_max = win_rate
                curr_move = move
        print("Move", curr_move, "Is the best option, with win rate", curr_max)
        return curr_move

    def send_training_set(self):
        scores = []
        hands = []
        centers = []
        values = []
        print('SEND TRAINING SET')
        for i in range(len(self.visited_states)):
            player_str, center_str = str(self.visited_states[i]['player']), str(self.visited_states[i]['center'])
            if (player_str, center_str) in self.plays:
                self.visited_states[i]['value'] = self.wins[(player_str, center_str)] / self.plays[(player_str, center_str)]
        for i in range(len(self.visited_states)):
            if 'value' not in self.visited_states[i]:
                continue
            state = self.visited_states[i]
            player, opponent, center, value = state['player'], state['opponent'], state['center'], state['value']
            _score, _hand, _center = self.nn.stateToInput(player, opponent, center)
            if i == 0:
                scores = np.expand_dims(_score, axis=0)
                hands = np.expand_dims(_hand, axis=0)
                centers = np.expand_dims(_center, axis=0)
            else:
                scores = np.append(scores, np.expand_dims(_score, axis=0), axis=0)
                hands = np.append(hands, np.expand_dims(_hand, axis=0), axis=0)
                centers = np.append(centers, np.expand_dims(_center, axis=0), axis=0)
            values = np.append(values, value)
        self.nn.trainNetwork(scores, hands, centers, values)