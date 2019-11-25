import csv
import traceback
import networkx as nx

def promptUserInput(message, inputType):
    """ask the user to enter an input"""
    # message: message to display to the user regarding what input to place
    # inputType: expected input type. either 'int', 'float' or 'str'
    userInput = None
    try:
        while True:
            userInput = input(message)
            try:
                if inputType is 'int':
                    userInput = int(userInput.strip())
                elif inputType is 'float':
                    userInput = float(userInput.strip())
                elif inputType is 'str':
                    userInput = str(userInput.strip())
                    if '.csv' not in userInput:
                        raise TypeError
                break
            except (ValueError, TypeError):
                print('Invalid input. Please try again.')
    except:
        userInput = None
        err = str(traceback.format_exc())
        raise FunctionCallError(err)
    finally:
        return userInput

def extractEdgesFromCSV(Graph, fname):
    """extract edges information from the csv file"""
    # Graph: graph that will be populated
    # fname: input csv file containing edges
    edges = []
    try:
        # add the nodes, edges, edge weight and color
        assert Graph is not None, 'Graph is not instantiated.'
        with open(fname) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                node1 = int(row[0].strip())
                node2 = int(row[1].strip())
                weight = float(row[2].strip())
                color = str(row[3].strip())
                edge = (node1, node2, {'weight': weight, 'color': color})
                edges.append(edge)
        Graph.add_edges_from(edges)
    except:
        Graph = None
        err = str(traceback.format_exc())
        raise FunctionCallError(err)

def findAllPaths(A, B, Graph, visitedDict, currentPathList, allPathsList):
    """Recursive function implementing Depth First Search Algorithm to find all possible paths
        between node A and node B from graph G."""
    # A: starting node or current node
    # B: ending node
    # Graph: Graph filled with nodes and edges
    # visitedList: list of nodes that have already been visited
    # currentPathList: list of the current path being searched for
    # allPathsList: list of all possible paths between start node and end node
    try:
        # add node A to the visitedList and currentPathList
        visitedDict[str(A)] = True
        currentPathList.append(A)
##        print('Current path list:')
##        print(currentPathList)

        # if node A is the end node B, add currentPathList to allPathsList
        if A == B:
            allPathsList.append(currentPathList[:])
##            print('Completed a path:')
##            print(allPathsList)

        # if A is not the end node B, check for adjacent nodes of A and go to a node that has not been visited
        else:
            adjacentNodes = list(Graph.adj[A])
            for node in adjacentNodes:
                if str(node) not in visitedDict:
                    findAllPaths(node, B, Graph, visitedDict, currentPathList, allPathsList)

        # when a path is found or all nodes in adjacentNodes are exhausted,
        # remove current node from currentPathList and from visitedList
        currentPathList.pop()
        visitedDict.pop(str(A))

    except:
        err = str(traceback.format_exc())
        raise FunctionCallError(err)


def convertToTuple(list):
    """Convert a list of integers into a list of tuples. ie. [1,2,3,4,5] ----> [(1,2), (2,3), (3,4), (4,5)] """
    # list: list of nodes/integers
    tupleList = []
    try:
        listLen = len(list)
        for i in range(0, listLen - 1):
            tupleEntry = (list[i], list[i+1])
            tupleList.append(tupleEntry)
    except:
        err = str(traceback.format_exc())
        raise FunctionCallError(err)
    finally:
        return tupleList

def applyPredicates(allPaths, A, B, Graph, C, D, fName):
    """Apply predicates to all path in the allPathsList. Output the path to csv file if it passes all predicates."""
    # allPaths: list of a list. sublist contains tuples for each edge
    # A: starting node
    # B: ending node
    # Graph: populated Graph
    # C: exact number of nodes that a path solution can have
    # D: minimum weight that a path solution can have
    # fName: name of output csv file
    try:
        passCount = 0
        for path in allPaths:
            passedIsPath = is_path(path, A, B, Graph)
            passedTotalWeight = total_weight(path, D, Graph)
            passedNumOfNodes = no_nodes(path, C)
            if passedIsPath and passedTotalWeight and passedNumOfNodes:
                # if a path passes all predicates, output the edges of the path to csv file
                passCount += 1
                if passCount == 1:
                    # if the path is the first pass, create a new output file
                    outputToCSV(path, passCount, fName, 'w')
                else:
                    # append to existing output file
                    outputToCSV(path, passCount, fName, 'a')

        # if no paths were valid solutions, print NULL to output file
        if passCount == 0:
            outputToCSV([], passCount, fName, 'w')
    except:
        err = str(traceback.format_exc())
        raise FunctionCallError(err)

def outputToCSV(path, pathNum, fName, fType):
    """Output a path to a csv file."""
    # path: list of edge tuples
    # pathNum: passing number assigned to this path
    # fName: name of output csv file
    # fType: either 'a' for appending to existing file or 'w' for writing to a new file
    try:
        assert pathNum != 0, 'No valid path solution.'
        header = 'path_{}'.format(str(pathNum))
        with open(fName, fType, newline='') as f:
            writer = csv.writer(f)
            writer.writerow([header])
            writer.writerows(path)

    # write 'NULL' to csv output if no valid paths
    except AssertionError as err:
        print(str(err))
        header = 'NULL'
        with open(fName, fType, newline='') as f:
            writer = csv.writer(f)
            writer.writerow([header])
    except:
        err = str(traceback.format_exc())
        raise FunctionCallError(err)

##### predicates #####
def is_path(s, a, b, Graph):
    """returns true if s is a path between node a and node b"""
    result = False
    try:
        assert Graph is not None, 'Graph is not instantiated.'
        assert s is not None, 'Set contains no edges.'

        # make sure that a is the starting node and b is the ending node of the set s
        assert s[0][0] == a, '{} is not the starting node in the set of edges.'.format(a)
        assert s[-1][1] == b, '{} is not the ending node in the set of edges.'.format(b)

        edgeListLen = len(s)
        currNode1 = None
        currNode2 = None
        prevNode2 = None
        for i in range(0, edgeListLen):
            currNode1 = s[i][0]
            currNode2 = s[i][1]
            if i != 0:
                # make sure that the first node of the current edge is equal to the second node of the previous edge
                assert currNode1 == prevNode2, 'First node of current edge does not match second node of last edge.'

            # make sure edge exists in the Graph. Throws KeyError if edge does not exist
            try:
                edgeInfo = Graph.edges[currNode1, currNode2]
                result = True
            except KeyError as err:
                raise FunctionCallError(err)

            # store the second node for later comparison
            prevNode2 = currNode2

    except:
        result = False
        err = str(traceback.format_exc())
        raise FunctionCallError(err)
    finally:
        print('Set of edges: ')
        print(s)
        print('is_path = {}'.format(result))
        return result

def total_weight(s, n, Graph):
    """returns true if total weight of edges in set s is greater than n"""
    result = False
    try:
        # add up the total weight of the edges
        totalWeight = 0
        for edge in s:
            node1 = edge[0]
            node2 = edge[1]
            weight = Graph.edges[node1, node2]['weight']
            totalWeight += weight

        # compare the added weight to n
        if totalWeight > n:
            result = True
    except:
        result = False
        err = str(traceback.format_exc())
        raise FunctionCallError(err)
    finally:
        print('Set of edges: ')
        print(s)
        print('total_weight = {}'.format(result))
        return result

def no_nodes(s, n):
    """returns true if the number of nodes of s is exactly n"""
    result = False
    try:
        numOfNodes = int(n)
        nodesDict = {}
        for edge in s:
            for node in edge:
                key = str(node)
                nodesDict[key] = True
        if len(nodesDict) == numOfNodes:
            result = True
    except:
        result = False
        err = str(traceback.format_exc())
        raise FunctionCallError(err)
    finally:
        print('Set of edges: ')
        print(s)
        print('no_nodes = {}'.format(result))
        return result

##### custom exceptions #####
class FunctionCallError(Exception):
    """FunctionCallError is raised back to the main function from the callee function"""
    pass
