import networkx as nx
import random

# REQUIRES PRESET ADJACENCY MATRIX
class GridLayout:
    def __init__(self, n, m, numNodes, adjMatrix):
        self.n = n 
        self.m = m
        self.numNodes = numNodes   
        self.adjMatrix = adjMatrix
        self.G = self.createGraphFromMatrix()

    def createGraphFromMatrix(self):
        G = nx.Graph()
        rows, cols = self.n, self.m
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j
                if j < cols - 1:
                    rightNeigh = node + 1
                    weight = self.adjMatrix[node][rightNeigh]
                    # should never happen
                    if weight == None:
                        print(f"ERROR: INVALID EDGE {node, rightNeigh}")
                    G.add_edge(node, rightNeigh, weight = weight)
                
                if i < rows - 1:
                    botNeigh = (i + 1) * cols + j 
                    weight = self.adjMatrix[node][botNeigh]
                    # should never happen
                    if weight == None:
                        print(f"ERROR: INVALID EDGE {node, botNeigh}")
                    G.add_edge(node, botNeigh, weight = weight)
        return G

# USED ONLY FOR RANDOMNESS
class RandomGridLayout:
    def __init__(self, n, m, numNodes, durationRange):
        self.n = n 
        self.m = m
        self.numNodes = numNodes
        self.minDuration, self.maxDuration = durationRange
        self.G = self.createGraph()
        self.adjMatrix = self.createAdjMatrix(numNodes, self.G)
        
    # creates a grid system graph
    def createGraph(self):
        G = nx.Graph()
        rows, cols = self.n, self.m
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j
                if j < cols - 1:
                    rightNeigh = node + 1
                    weight = random.randint(self.minDuration, self.maxDuration)
                    G.add_edge(node, rightNeigh, weight = weight)
                
                if i < rows - 1:
                    botNeigh = (i + 1) * cols + j 
                    weight = random.randint(self.minDuration, self.maxDuration)
                    G.add_edge(node, botNeigh, weight = weight)
        return G
    
    def createAdjMatrix(self, numNodes, G):
        adjMatrix = [[None for _ in range(numNodes)] for _ in range(numNodes) ]
        seen = set()
        for i in range(numNodes):
            for j in range(numNodes):
                if G.has_edge(i, j) and (j, i) not in seen and i != j:
                    duration = G[i][j]['weight']
                    adjMatrix[i][j] = duration
                    adjMatrix[j][i] = adjMatrix[i][j]
                seen.add((i, j))
        return adjMatrix

