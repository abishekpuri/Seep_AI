# Seep_AI
Building An AI Agent to play two-player version of Seep

To play the game, run python Game.py

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
  
For example, run ```/usr/local/bin/python3 minimaxGame.py -d1 1 -d2 1 -l 1 1 1 100 -r 10 -c 0 -m 1 -d results/```.

WARNING: Please prepare the directory structure before running the command. The root folder name is an argument above. The subfolder must be named ```gameResult```.
```
results/
└── gameResult
```
