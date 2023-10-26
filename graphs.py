import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.patches import *
from collections import defaultdict

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
    def displayGraphDrivers(self, drivers):
        pos = {}
        colorList = ['green','red','cyan','magenta','yellow','tomato', 'orchid', 'olive','purple','lime',
            'orange','pink', 'violet','crimson','coral','gold','silver', 'khaki','maroon','turquoise']
        
        colorMapping = {node: 'skyblue' for node in self.G.nodes()}

        label_mapping = {node: [] for node in self.G.nodes()}

        for i, driver in enumerate(drivers):
            if driver.currLoc in colorMapping:
                colorMapping[driver.currLoc] = colorList[i % len(colorList)]
                label_mapping[driver.currLoc].append(str(driver.id))
                
        for node in label_mapping:
            label_mapping[node] = ','.join(label_mapping[node]) if label_mapping[node] else str(node)

        colors = [colorMapping[node] for node in self.G.nodes()]

        for node in self.G.nodes():
            row = node // self.m
            col = node % self.m
            pos[node] = (col, -row)  

        plt.subplots(figsize=(15, 15)) 
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        plt.title(f'{self.m}x{self.n} Grid Simulation with Driver Start Locations') 
        nx.draw(self.G, pos, labels=label_mapping, node_color=colors, with_labels=True, node_size=700, font_size=13)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=12)
        plt.show()
        
    def displayGraphOrders(self, orders):
        pos = {}
        nodeInfo = defaultdict(lambda: {'pickup': 0, 'dropoff': 0})

        for node in self.G.nodes():
            row = node // self.m
            col = node % self.m
            pos[node] = (col * 2, -row * 2)  # Multiply by 2 to increase spacing

        for order in orders:
            if order.pickup in pos:
                nodeInfo[order.pickup]['pickup'] += 1
            if order.dropoff in pos:
                nodeInfo[order.dropoff]['dropoff'] += 1

        _, ax = plt.subplots(figsize=(12,12))

        plt.title(f'{self.m}x{self.n} Grid Simulation with Orders')
        nx.draw(self.G, pos, ax=ax, with_labels=False, node_color='none', edgecolors='none', node_size=0, font_size=18)

        for node in self.G.nodes():
            x, y = pos[node]
            info = nodeInfo[node]
            total = info['pickup'] + info['dropoff']

            pickupFrac = info['pickup'] / (total if total else 1)
            dropoffFrac = info['dropoff'] / (total if total else 1)

            # shades of green/red darken based on pickup/dropoff count
            greenShade = max(0.9 - 0.1 * info['pickup'], 0.5)
            redShade = max(0.9 - 0.1 * info['dropoff'], 0.5)

            if pickupFrac > 0 and dropoffFrac > 0:
                ax.add_patch(Wedge((x, y), 0.4, 0, 360 * pickupFrac, facecolor=(0, greenShade, 0), edgecolor='black', linewidth=0, zorder=2))
                ax.add_patch(Wedge((x, y), 0.4, 360 * pickupFrac, 360, facecolor=(redShade, 0, 0), edgecolor='black', linewidth=0, zorder=2))
            elif pickupFrac > 0:
                ax.add_patch(Circle((x, y), 0.4, facecolor=(0, greenShade, 0), edgecolor='black', linewidth=0, zorder=2))
            elif dropoffFrac > 0:
                ax.add_patch(Circle((x, y), 0.4, facecolor=(redShade, 0, 0), edgecolor='black', linewidth=0, zorder=2))
            else:
                ax.add_patch(Circle((x, y), 0.4, facecolor='skyblue', edgecolor='black', linewidth=0, zorder=2))
        nx.draw(self.G, pos, ax=ax, with_labels=True, node_color='none', edgecolors='none', node_size=300, font_size=7)
        plt.legend([Wedge((0, 0), 1, 0, 1, facecolor='green'), Wedge((0, 0), 1, 0, 1, facecolor='red'), Circle((0, 0), color='skyblue')], 
                ['Order Pickup', 'Order Dropoff', 'No Order'], loc="upper left")

        edgeLabels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edgeLabels, font_size=12)
        plt.axis('equal')
        plt.show()

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

