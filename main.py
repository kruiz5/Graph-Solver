import os
import sys
import traceback
import networkx as nx
from function import *


def main():
    try:
        # fill the graph based on user input csv file
        Graph = nx.Graph()
        assert sys.argv[1] is not None, 'No argument passed for csv input.'
        fp = str(sys.argv[1])
        assert os.path.exists(fp) is True, 'CSV file does not exist.'
        extractEdgesFromCSV(Graph, fp)
        assert Graph is not None or Graph.number_of_nodes() != 0, 'Graph is not instantiated and has no nodes.'

        # ask user to input the following parameters
        A = promptUserInput('Enter the starting node: ', 'int')
        B = promptUserInput('Enter the ending node: ', 'int')
        C = promptUserInput('Enter the exact number of nodes a solution should have: ', 'int')
        D = promptUserInput('Enter the minimum weight a solution should have: ', 'float')
        outputFile = promptUserInput('Enter the name of the output csv file: ', 'str')

        assert A is not None, 'User did not enter a valid starting node.'
        assert B is not None, 'User did not enter a valid ending node.'
        assert C is not None, 'User did not enter a valid number of nodes.'
        assert D is not None, 'User did not enter a valid minimum weight.'
        assert outputFile is not None and '.csv' in outputFile, 'User did not enter a valid output file.'

        # find all possible paths from A to B and store each path in allPathsList
        visitedDict = {}
        currentPathList = []
        allPathsList = []  # [[1,2,5,..,4], [1,3,2,...,4], [1,2,3,...,4], ...]
        findAllPaths(A, B, Graph, visitedDict, currentPathList, allPathsList)

##        print(allPathsList)

        # convert each path list in allPathsList into tuple form
        allPathListTuple = []  # [[(1,2),(2,5),...], ...]
        for pathList in allPathsList:
            tupleList = convertToTuple(pathList)
            allPathListTuple.append(tupleList)

        print(allPathListTuple)

        # apply the predicates to allPathListTuple and write valid paths to output csv
        applyPredicates(allPathListTuple, A, B, Graph, C, D, outputFile)

    except:
        print(traceback.format_exc())
        exit()


if __name__ == '__main__':
    main()
