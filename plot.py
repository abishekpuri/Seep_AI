import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import argparse
import re

resultDirName = 'results'
# resultDir = 'results/'
gameStatDir = 'gameResult/'
scoresFile = 'scores.csv'
gameFile = 'gameplay'
totalPlot = 24 # hardcode

def plotScore(dirName, title):
    # plot
    try:
        scoresDf = pd.read_csv(dirName+scoresFile, index_col=0)
        print("Type 1: Final scores")
        ax = scoresDf.plot(kind='line', xticks=np.arange(scoresDf.shape[0]), title=title)
        ax.set_xlabel("Game")
        ax.set_ylabel("Final scores")
        # print win rate
        wins = scoresDf.apply(lambda x: x.MCTS > x.Expectiminimax, axis=1)
        wins = wins.sum()
        print(title)
        print('Win => MCTS:expectiminimax = %i:%i' % (wins,scoresDf.shape[0]-wins))
    except:
        pass
        # print('No file')

# Global constant for the setting
depthOfMinimax = [1, 2]
penaltyOfSeep = [1, 50, 100]
roundOfMCTS = [750, 1000, 1250, 1500]
def getTitleFromInt(i):
    if i <= 12: # hardcode
        depth = depthOfMinimax[0]
    else:
        depth = depthOfMinimax[1]
        i-=12
    p = penaltyOfSeep[(i-1)//4]
    r = roundOfMCTS[(i-1)%4]
    return "Using MCTS with round %i and expectiminimax with seep penality %i and minimax search depth %i" % (r, p, depth)

def plotRandom(dirName, title):
    # Random gameplay dmeo
    randomFile = gameFile+str(random.randint(0, 49))+'.csv' # hardcode
    print('Getting random file %s in %s' % (randomFile, dirName))
    try:
        detailDf = pd.read_csv(dirName+gameStatDir+randomFile, index_col=0)

        # split 4 columns and merge score
        expectiminimax = detailDf.iloc[:, 0]
        expectiminimaxGameScore = detailDf.iloc[:, 1]
        mcts = detailDf.iloc[:, 2]
        mctsGameScore = detailDf.iloc[:, 3]
        scores = pd.concat([expectiminimaxGameScore, mctsGameScore], axis=1)
        print(scores)

        # show 3 graphs, emm, mcts, and both scores
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15,5))
        fig.suptitle(randomFile+' in '+title)

        ax = mcts.plot(ax=axes[0], kind='line', xticks=np.arange(24), title="MCTS")
        ax.set_xlabel("Move")
        ax.set_ylabel("Win rate")
        ax = expectiminimax.plot(ax=axes[1], kind='line', xticks=np.arange(24), title="Expectiminimax")
        ax.set_xlabel("Move")
        ax.set_ylabel("Score")
        ax = scores.plot(ax=axes[2], kind='line', xticks=np.arange(24), title="MCTS vs Expectiminimax")
        ax.set_xlabel("Move")
        ax.set_ylabel("Game Score")
    except:
        print('No file')

def getAverage(dirName):
    try:
        scoresDf = pd.read_csv(dirName+scoresFile, index_col=0)
        wins = scoresDf.apply(lambda x: x.MCTS > x.Expectiminimax, axis=1)
        average = wins.mean()
        return average
    except:
        # print('No file')
        return None

def plotAverage():
    for i in range(len(depthOfMinimax)):
        for j in range(len(penaltyOfSeep)):
            averages = []
            for k in range(len(roundOfMCTS)):
                resultNum = 12*i+j*4+k+1
                averages.append(getAverage(resultDirName+str(resultNum)+'/'))
            series = pd.DataFrame({'Average win rate': averages}, index=roundOfMCTS)
            seriesNoNa = series.dropna()
            print(seriesNoNa)
            if not seriesNoNa.empty:
                ax = series.plot(kind='line', xticks=roundOfMCTS, title='Versus expectiminimax with penalty %i and minimax depth %i' % (penaltyOfSeep[j], depthOfMinimax[i]))
                ax.set_xlabel("Number of rounds in MCTS")
                ax.set_ylabel("Average win rate")

def plotType(typeOfPlot, dirName):
    if typeOfPlot == 1:
        if args.d:
            resultDir = args.d
            resultNum = int(re.search(r'\d+', resultDir).group())
            # print(resultNum)
            plotScore(resultDir, getTitleFromInt(resultNum))
        else:
            for i in range(1, totalPlot+1):
                resultDir = resultDirName + str(i)+'/'
                title = getTitleFromInt(i)
                plotScore(resultDir, title)
    elif typeOfPlot == 2:
        print("Type 2: random game")
        if args.d:
            resultDir = args.d
            resultNum = int(re.search(r'\d+', resultDir).group())
            # print(resultNum)
            plotRandom(resultDir, getTitleFromInt(resultNum))
        else:
            for i in range(1, totalPlot+1):
                resultDir = resultDirName + str(i)+'/'
                title = getTitleFromInt(i)
                plotRandom(resultDir, title)
    elif typeOfPlot == 3:
        print("Type 3: Average performance")
        plotAverage()


parser = argparse.ArgumentParser()
parser.add_argument("-t", help='Type of plots', required=True, type=int, choices=[1, 2, 3])
parser.add_argument("-d", help='Results directory', type=str)
parser.add_argument('-p', help='Plot', action='store_true')
args = parser.parse_args()

plotType(args.t, args.d)
if args.p:
    plt.show()