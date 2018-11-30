from Classes import NeuralNetwork
from random import choice
import copy
import time
import math
import numpy as np

winRateHistory = []

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

    def predictions_nn(self, center, player, opponent, notplayed):
        predictions = []
        _moves = []
        _inputs = []
        for index, move in enumerate(notplayed):
            new_player, new_center = self._next_state(center, player, move)
            _input = self.nn.state2input(new_player, opponent, new_center)
            if index == 0:
                _inputs = np.expand_dims(_input, axis=0)
            else:
                _inputs = np.append(_inputs, np.expand_dims(_input, axis=0), axis=0)
            _moves.append(move)
        _values = self.nn.predict_input_values(_inputs)[0]
        for i in range(len(_values)):
            predictions.append((_values[i], _moves[i]))
        return predictions

    def predictions_from_nn(self, center, player, opponent):
        _moves = []
        predictions = []
        _inputs = []
        for index, move in enumerate(player.moves):
            new_player, new_center = self._next_state(center, player, move)
            _input = self.nn.state2input(new_player, opponent, new_center)
            if index == 0:
                _inputs = np.expand_dims(_input, axis=0)
            else:
                _inputs = np.append(_inputs, np.expand_dims(_input, axis=0), axis=0)
            _moves.append(move)

        print(_inputs)

        _values = self.nn.predict_input_values(_inputs)[0]
        # print("What is values.sahpe {} ".format(_values.shape))
        # print(_values)
        for i in range(len(_values)):
            predictions.append((_values[i], _moves[i]))
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
        while len(p1.hand) > 0 or len(p2.hand) > 0:
            # generate all possible moves
            p1.possibleMoves(center, bidMove, bid)
            # if no moves, break
            if len(p1.moves) == 0:
                break
            # generate next states of possible moves
            next_states = {str(move): self.next_state(center, p1, move) for move in p1.moves}
            win_rates = []
            notplayed = []
            predictions = []
            for move in p1.moves:
                played = plays.get(next_states[str(move)])
                if played:
                    win_rate = wins[next_states[str(move)]] / played
                    win_rates.append((win_rate, move))
                else:
                    notplayed.append(move)
            print('notplayed')
            print(notplayed)
            if len(notplayed) != 0:
                predictions = self.predictions_nn(center, p1, p2, notplayed)
            print('predictions')
            print(predictions)
            values = win_rates + predictions
            print('values')
            print(values)
            for e in values:
                if np.isnan(e[0]):
                    v = e[1]
                    values.remove(e)
                    values.append((0,v))
            maximum = max(values, key=lambda x: x[0])[0]
            if maximum == 0:
                p1move = choice(p1.moves)
            else:
                for e in values:
                    k = e[0] / maximum
                    v = e[1]
                    values.remove(e)
                    values.append((k, v))
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
        while time.time() - currTime < 5:
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
        winRateHistory.append(curr_max)
        return curr_move

    def get_training_set(self):
        _inputs = []
        values = []
        print('Generate training set')
        for i in range(len(self.visited_states)):
            player_str, center_str = str(self.visited_states[i]['player']), str(self.visited_states[i]['center'])
            if (player_str, center_str) in self.plays:
                self.visited_states[i]['value'] = self.wins[(player_str, center_str)] / self.plays[(player_str, center_str)]
        for i in range(len(self.visited_states)):
            if 'value' not in self.visited_states[i]:
                continue
            state = self.visited_states[i]
            player, opponent, center, value = state['player'], state['opponent'], state['center'], state['value']
            _input = self.nn.state2input(player, opponent, center)
            if i == 0:
                _inputs = np.expand_dims(_input, axis=0)
            else:
                _inputs = np.append(_inputs, np.expand_dims(_input, axis=0), axis=0)
            values = np.append(values, value)
        return _inputs, values
        # self.nn.train_network(_inputs, values)
