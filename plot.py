import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

resultDir = 'results/'
gameStatDir = 'gameResult/'
scoresFile = 'scores.csv'

scoresDf = pd.read_csv(resultDir+scoresFile, index_col=0)
MCTS10s = scoresDf[:10]
MCTS20s = scoresDf[10:].reset_index(drop=True)
print(MCTS20s)
ax = MCTS10s.plot(kind='line', xticks=np.arange(10), title='Expectiminimax vs MCTS with 10s')
ax.set_xlabel("Game")
ax.set_ylabel("Final scores")
ax = MCTS20s.plot(kind='line', xticks=np.arange(10), title='Expectiminimax vs MCTS with 20s')
ax.set_xlabel("Game")
ax.set_ylabel("Final scores")
plt.show()