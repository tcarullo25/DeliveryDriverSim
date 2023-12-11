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

        labelMapping = {node: [] for node in self.G.nodes()}

        for i, driver in enumerate(drivers):
            if driver.currLoc in colorMapping:
                colorMapping[driver.currLoc] = colorList[i % len(colorList)]
                labelMapping[driver.currLoc].append(str(driver.id))
                
        for node in labelMapping:
            labelMapping[node] = ','.join(labelMapping[node]) if labelMapping[node] else str(node)

        colors = [colorMapping[node] for node in self.G.nodes()]

        for node in self.G.nodes():
            row = node // self.m
            col = node % self.m
            pos[node] = (col, -row)  

        plt.subplots(figsize=(15, 15)) 
        edgeLabels = nx.get_edge_attributes(self.G, 'weight')
        plt.title(f'{self.m}x{self.n} Grid Simulation with Driver Start Locations') 
        nx.draw(self.G, pos, labels=labelMapping, node_color=colors, with_labels=True, node_size=700, font_size=13)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edgeLabels, font_size=12)
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

    def displayOrderRoute(self, orderLog, order):
        if not order.driver:
            print(f"ERROR: {order.id} does not have a driver\n")
            return 
    
        fig, ax = plt.subplots(figsize=(15, 15))

        pos = {node: (node % self.m, -(node // self.m)) for node in self.G.nodes()} 
        
        availableDrivers = orderLog[order.id]

        fig.text(0, .985, "Available Drivers Info:", fontsize=11, ha='left', transform=fig.transFigure)
        for i, (driver, reputation, _, acceptedDrivers) in enumerate(availableDrivers):
            if driver.id in acceptedDrivers:
                status = 'Accepted'
            else:
                status = 'Rejected'
            driverInfo = f"Driver {driver.id}: {driver.policy}\nOrder Status: {status}\nCluster Hover: {driver.policy.clusterHover}\nCurrent Reputation: {reputation}"
            fig.text(0, .99 - (i+1)*0.065, driverInfo, fontsize=9, ha='left', transform=fig.transFigure)

        nodeColors = {node: 'skyblue' for node in self.G.nodes()}
        orderDriverCurrLoc = None
        labels = {node: str(node) for node in self.G.nodes()}
        for (driver, _, currLoc, _) in availableDrivers:
            if currLoc in labels:
                labels[currLoc] = f"{driver.id}"
            if driver.id == order.driver.id:
                nodeColors[currLoc] = 'purple'
                orderDriverCurrLoc = currLoc
            else:
                nodeColors[currLoc] = 'magenta' if currLoc != orderDriverCurrLoc else 'purple'

        if orderDriverCurrLoc in labels:
            labels[orderDriverCurrLoc] = f"{order.driver.id}"

        orderRoute = nx.shortest_path(self.G, source=order.pickup, target=order.dropoff, weight = 'weight')
        routeEdges = [(orderRoute[i], orderRoute[i+1]) for i in range(len(orderRoute)-1)]
        
        driverToPickupEdges = []
        driverToPickupRoute = nx.shortest_path(self.G, source=orderDriverCurrLoc, target=order.pickup, weight = 'weight')
        driverToPickupEdges = [(driverToPickupRoute[i], driverToPickupRoute[i+1]) for i in range(len(driverToPickupRoute)-1)]

        nodeColors[order.pickup] = 'green' if order.pickup != orderDriverCurrLoc else nodeColors[order.pickup] 
        nodeColors[order.dropoff] = 'red' if order.dropoff != orderDriverCurrLoc else nodeColors[order.dropoff]

        nx.draw_networkx_nodes(self.G, pos, ax=ax, node_color=[nodeColors[node] for node in self.G.nodes()])
        nx.draw_networkx_edges(self.G, pos, ax=ax, edgelist=driverToPickupEdges, edge_color='blue', width=2)
        nx.draw_networkx_edges(self.G, pos, ax=ax, edgelist=routeEdges, edge_color='orange', width=2)
        nx.draw_networkx_edges(self.G, pos, ax=ax, edgelist=set(self.G.edges()) - set(routeEdges) - set(driverToPickupEdges), edge_color='gray')
        
        nx.draw_networkx_labels(self.G, pos, ax=ax, labels=labels)
        edgeLabels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edgeLabels, font_size=10)
        legendElements = [
            plt.Line2D([0], [0], color='blue', linewidth=2, label='Driver to Pickup'),
            plt.Line2D([0], [0], color='orange', linewidth=2, label='Pickup to Dropoff'),
            plt.Line2D([0], [0], color='magenta', marker='o', linestyle='None', markersize=5, label='Available Driver'),
            plt.Line2D([0], [0], color='purple', marker='o', linestyle='None', markersize=5, label='Chosen Driver'),
            plt.Line2D([0], [0], color='green', marker='o', linestyle='None', markersize=5, label='Pickup Node'),
            plt.Line2D([0], [0], color='red', marker='o', linestyle='None', markersize=5, label='Dropoff Node')
        ]
        plt.legend(handles=legendElements, loc='upper left', fontsize='small')


        plt.suptitle(f"Order Route for Order {order.id}", y = .96)
        plt.title(f"Price accepted at: {round(order.price, 2)}\nAccepted {order.additionalCompensation} minutes after sending out to drivers\nNOTE: Some information may be hidden/overlapped by other highlighted nodes", fontsize=8)
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

