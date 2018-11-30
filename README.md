# Seep_AI
Building An AI Agent to play two-player version of Seep

To play the game, 
```
usage: Game.py [-h] [-d1 D1] [-d2 D2] [-l L L L L] [-r R] {mcts,emm,nn}

positional arguments:
  {mcts,emm,nn}  Type of agent

optional arguments:
  -h, --help     show this help message and exit
  -d1 D1         Depth in expectimax
  -d2 D2         Depth in minimax
  -l L L L L     Weights in evaluation function
  -r R           Round in MCTS
```
For example, run ```python Game.py mcts -r 1500``` to play a game with MCTS using 1500 game simulation per move. :)

# File structure
```
.
├── Classes                                             Classes for the game, AI and model
├── Game.py                                             Python script for human versus computer
├── MCTSGame.py                                         Python script for MCTS versus MCTS                                           
├── minimaxGame.py                                      Python script for expectiminimax versus MCTS
├── minivsnnGame.py                                     Python script for expectiminimax versus nnMCTS
├── nnGame.py                                           Python script for training the neutral network
├── plot.py                                             Plot the results
└── README.md
```

# For MCTS vs MCTS
Run ```python MCTSGame.py```.

NOTE: Please kindly choose the bid and do the first move for the MCTS model.

# For expectiminimax vs MCTS
```
usage: minimaxGame.py [-h] -d1 D1 -d2 D2 -l L L L L -r R -c C -m M -d D

optional arguments:
  -h, --help  show this help message and exit
  -d1 D1      Depth in expectimax
  -d2 D2      Depth in minimax
  -l L L L L  Weights in evaluation function
  -r R        Round in MCTS
  -c C        Current gameplay
  -m M        Maximun gameplay
  -d D        Results directory
```
WARNING: Please prepare the directory structure before running the command. The root folder name is an argument above. The subfolder must be named ```gameResult```.
```
results/
└── gameResult
```
### Exmaple
For example, run ```/usr/local/bin/python3 minimaxGame.py -d1 1 -d2 1 -l 1 1 1 100 -r 10 -c 0 -m 1 -d results/```.

# For plotting results
```
usage: plot.py [-h] -t {1,2,3} [-d D] [-p]

optional arguments:
  -h, --help  show this help message and exit
  -t {1,2,3}  Type of plots
  -d D        Results directory
  -p          Plot
```
NOTE: If results directory is not given, all results will be shown.
### Types
1. Type 1 shows final scores
2. Type 2 shows a random game statistic
3. Type 3 shows average win rate of MCTS
### Example
For example, run ```python plot.py -t 3 -p``` with graphs and ```python plot.py -t 3``` without graphs
