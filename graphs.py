import networkx as nx
import random

MAX_DURATION = 30

# USED ONLY FOR RANDOMNESS
def createAdjMatrix(numNodes, G):
    adjMatrix = [[None for _ in range(numNodes)] for _ in range(numNodes) ]
    seen = set()
    for i in range(numNodes):
        for j in range(numNodes):
            if G.has_edge(i, j) and (j, i) not in seen and i != j:
                adjMatrix[i][j] = random.randint(5, MAX_DURATION)
                adjMatrix[j][i] = adjMatrix[i][j]
            seen.add((i, j))
    return adjMatrix

class GridLayout:
    def __init__(self, n, m, numNodes):
        self.n = n 
        self.m = m
        self.G = self.createGraph()
        self.adjMatrix = createAdjMatrix(numNodes, self.G)
        self.numNodes = numNodes

    # creates a grid system graph
    def createGraph(self):
        G = nx.Graph()
        rows, cols = self.n, self.m
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j
                if j < cols - 1:
                    rightNeigh = node + 1
                    G.add_edge(node, rightNeigh)
                
                if i < rows - 1:
                    botNeigh = (i + 1) * cols + j 
                    G.add_edge(node, botNeigh)
        return G

