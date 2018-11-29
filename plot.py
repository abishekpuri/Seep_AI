import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

resultDir = 'results/'
gameStatDir = 'gameResult/'
scoresFile = 'scores.csv'

scoresDf = pd.read_csv(resultDir+scoresFile, index_col=0)
MCTS10s = scoresDf[:10]
MCTS20s = scoresDf[10:].reset_index(drop=True)
# print(MCTS20s)
ax = MCTS10s.plot(kind='line', xticks=np.arange(10), title='Expectiminimax vs MCTS with 10s')
ax.set_xlabel("Game")
ax.set_ylabel("Final scores")
ax = MCTS20s.plot(kind='line', xticks=np.arange(10), title='Expectiminimax vs MCTS with 20s')
ax.set_xlabel("Game")
ax.set_ylabel("Final scores")

# Random gameplay dmeo
randomFile = 'gameplay'+str(random.randint(0, 9))+'.csv' # mstc 10s
print('Getting random file %s' % randomFile)
detailDf = pd.read_csv(resultDir+gameStatDir+randomFile, index_col=0)
# print(detailDf)
mcts = detailDf.iloc[:, 1]
expectiminimax = detailDf.iloc[:, 0]
# print(mcts)
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,5))
fig.suptitle(randomFile)

ax = mcts.plot(ax=axes[0], kind='line', xticks=np.arange(24), title="MCTS with 20s")
ax.set_xlabel("Move")
ax.set_ylabel("Win rate")
ax = expectiminimax.plot(ax=axes[1], kind='line', xticks=np.arange(24), title="Expectiminimax")
ax.set_xlabel("Move")
ax.set_ylabel("Score")

randomFile = 'gameplay'+str(random.randint(10, 19))+'.csv' # mstc 20s
print('Getting random file %s' % randomFile)
detailDf = pd.read_csv(resultDir+gameStatDir+randomFile, index_col=0)
# print(detailDf)
mcts = detailDf.iloc[:, 1]
expectiminimax = detailDf.iloc[:, 0]
# print(mcts)
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,5))
fig.suptitle(randomFile)

ax = mcts.plot(ax=axes[0], kind='line', xticks=np.arange(24), title="MCTS with 20s")
ax.set_xlabel("Move")
ax.set_ylabel("Win rate")
ax = expectiminimax.plot(ax=axes[1], kind='line', xticks=np.arange(24), title="Expectiminimax")
ax.set_xlabel("Move")
ax.set_ylabel("Score")

plt.show()