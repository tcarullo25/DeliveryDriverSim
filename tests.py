from graphs import *
from ordersAndDrivers import *
from driverPolicies import *
from collections import deque
import random

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# https://www.kosbie.net/cmu/spring-21/15-112/notes/notes-2d-lists.html
def format2dList(a):
    if (a == []):
        return "[]"
    
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    lines = []
    lines.append('[')
    for row in range(rows):
        line = ' [ '
        for col in range(cols):
            if (col > 0): line += ', '
            line += str(a[row][col]).rjust(fieldWidth)
        line += ' ]'
        if row < rows - 1:
            line += ','
        lines.append(line)
    lines.append(']')
    return '\n'.join(lines)

def genDropoff(randomMap, pickup, dropoffThreshold):
    availableDropoffs = []
    
    # BFS to get all available dropoffs within threshold
    q = deque([(pickup, 0)])
    visited = set()

    while q:
        currNode, currDur = q.popleft()

        if currNode not in visited:
            visited.add(currNode)

            for neighbor, dur in enumerate(randomMap.adjMatrix[currNode]):
                if dur != None:
                    totalDur = currDur + dur
                    if totalDur <= dropoffThreshold:
                        if neighbor != pickup:
                            availableDropoffs.append(neighbor)
                        q.append((neighbor, totalDur))

    if not availableDropoffs:
        print(f"ERROR: not enough dropoffs within the threshold {dropoffThreshold}")
        return
    
    # choose a random dropoff within the threshold
    return random.choice(availableDropoffs)

def genClusters(n, m, clusterSizeRange):
    lowerBound = max(1, n * m // 25)
    upperBound = max(lowerBound, n * m // 9)
    numClustersRange = (lowerBound, upperBound)
    numClusters = random.randint(*numClustersRange)
    clusters = []

    for _ in range(numClusters):
        clusterWidth = random.randint(*clusterSizeRange)
        clusterHeight = random.randint(*clusterSizeRange)
        maxTopLeftRow = n - clusterHeight
        maxTopLeftCol = m - clusterWidth

        if maxTopLeftRow <= 0 or maxTopLeftCol <= 0:
            # No space for cluster, skip
            continue

        topLeftRow = random.randint(0, maxTopLeftRow)
        topLeftCol = random.randint(0, maxTopLeftCol)

        clusters.append(((topLeftRow, topLeftCol), clusterWidth, clusterHeight))

    return clusters

def getDeliverTime(randomMap, pickup, dropoff):
    pickupToDropOff = nx.shortest_path(randomMap.G, 
                    source=pickup, target=dropoff, weight = 'weight')
    totalTime = 0
    for i in range(1, len(pickupToDropOff)):
        currNode, prevNode = pickupToDropOff[i], pickupToDropOff[i-1]
        duration = randomMap.adjMatrix[currNode][prevNode]
        totalTime += duration
    return totalTime

def genTest(testNum, n, m, basePay, numDrivers, durationRange, pickupTimeRange, orderSpawnRate, totalMins, dropoffThreshold=20, deliverTimeWiggleRoom=0, clusterSizeRange=(2, 3)):
    randomMap = RandomGridLayout(n, m, n * m, durationRange)                               
    orderCount = 0
    numNodes = n * m 
    orderQueue = []
    policies = ['rateFocused', 'greedy', 'reputationFocused']
    driverBehaviors = [1.1, 1.0, 0.9]
    drivers = [(i, random.randint(0, numNodes-1), random.choice(policies), random.choice(driverBehaviors)) for i in range(0, numDrivers)]
    clusters = genClusters(n, m, clusterSizeRange)
    clusterSpots = {cluster: [(row, col) 
                           for row in range(cluster[0][0], cluster[0][0] + cluster[2])
                           for col in range(cluster[0][1], cluster[0][1] + cluster[1])] 
                           for cluster in clusters}
    clustersWithoutPickup = set(clusterSpots.keys())
    for minute in range(totalMins):
        if random.random() < orderSpawnRate:
            #pickup = random.randint(0, numNodes-1)
            if clustersWithoutPickup:
                selectedCluster = random.choice(list(clustersWithoutPickup))
                clustersWithoutPickup.remove(selectedCluster)
            else:
                selectedCluster = random.choice(list(clusterSpots.keys()))
            
            pickupSpot = random.choice(clusterSpots[selectedCluster])
            pickupRow, pickupCol = pickupSpot
            pickup = pickupRow * m + pickupCol
            #(topLeftRow, topLeftCol), clusterWidth, clusterHeight = cluster
            #pickupRow = topLeftRow + random.randint(0, clusterHeight - 1)
            #pickupCol = topLeftCol + random.randint(0, clusterWidth - 1)
            #pickup = pickupRow * m + pickupCol

            dropoff = genDropoff(randomMap, pickup, dropoffThreshold)
            if dropoff == None: # could not meet threshold, exit
                return                                                      
            start, end = pickupTimeRange
            pickupTime = minute + random.randint(start, end) 
            deliverTime = pickupTime
            deliverTime += getDeliverTime(randomMap, pickup, dropoff) + deliverTimeWiggleRoom
            orderQueue.append((orderCount, pickup, dropoff, minute, pickupTime, deliverTime))
            orderCount += 1
    testFunction = \
    f'''
# TEST {testNum}
# LAYOUT: {n}x{m} GRID
# {numDrivers} DRIVERS, {totalMins//60} HOUR PERIOD
# FLAT RATE ${basePay}/order
# EDGE DURATIONS RANGE {durationRange}
# PICKUP TIME RANGE {pickupTimeRange}
# DELIVER TIME WIGGLE ROOM {deliverTimeWiggleRoom}
# DROPOFF THRESHOLD {dropoffThreshold}
# ACTIVE POLICIES: {policies}
def test{testNum}():
        n = {n}
        m = {m}
        basePay = {basePay} # total price will be calculated later when assigned to driver
        totalMins = {totalMins}
        adjMatrix = \\
        {format2dList(randomMap.adjMatrix)}
        map = GridLayout(n, m, n * m, adjMatrix)
        clusters = {clusters}
        policyDict = {{ 'rateFocused' : rateFocused, 'greedy' : greedy, 'reputationFocused' : reputationFocused }}
        orderInfo = \\
        {orderQueue}
        driverInfo = \\
        {drivers}
        orderQueue = []
        drivers = []
        # INIT ORDERS
        for id, pickup, dropoff, releaseTime, pickupTime, deliverTime in orderInfo:
            orderQueue.append(Order(id, pickup, dropoff, releaseTime, pickupTime, deliverTime, basePay))
        # INIT DRIVERS
        for id, start, policy, driverBehavior in driverInfo:
            driverPolicy = DriverPolicy(policy, policyDict[policy], random.choice([True, False]))
            drivers.append(Driver(id, start, driverPolicy, driverBehavior))

        return map, clusters, orderQueue, totalMins, drivers, basePay'''
    return testFunction

# TEST 1
# LAYOUT: 10x10 GRID
# 15 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $5/order
# EDGE DURATIONS RANGE (5, 10)
# PICKUP TIME RANGE (15, 25)
# DELIVER TIME WIGGLE ROOM 0
# DROPOFF THRESHOLD 20
# ACTIVE POLICIES: ['rateFocused', 'greedy', 'reputationFocused']
def test1():
        n = 10
        m = 10
        basePay = 5 # total price will be calculated later when assigned to driver
        totalMins = 360
        adjMatrix = \
        [
 [ None,    9, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    9, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    7, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    7, None,    5, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    5, None,    6, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    6, None,    8, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    8, None,   10, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,   10, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    7, None,    7, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [   10, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,   10, None, None, None, None, None, None, None, None,    9, None,   10, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    8, None, None, None, None, None, None, None, None,   10, None,    6, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    9, None, None, None, None, None, None, None, None,    6, None,    7, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    9, None, None, None, None, None, None, None, None,    7, None,   10, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    5, None, None, None, None, None, None, None, None,   10, None,    6, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    6, None,    7, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    8, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    6, None,    5, None, None, None, None, None, None, None, None,    9, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    5, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    9, None, None, None, None, None, None, None, None,    5, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    9, None,   10, None, None, None, None, None, None, None, None,    7, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,   10, None,    8, None, None, None, None, None, None, None, None,    6, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    8, None,    5, None, None, None, None, None, None, None, None, 
   8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,   10, None, None, None, None, None, None, None, 
None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,   10, None,    9, None, None, None, None, None, None, 
None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, 
None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, 
None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,   10, None,    8, None, None, None, 
None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    8, None,    6, None, None, 
None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None,    7, None, 
None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    7, None,    7, 
None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    7, None, 
   7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    7, 
None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, 
  10, None,    5, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, 
None,    5, None,    6, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, 
None, None,    6, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, 
None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, 
None, None, None, None,    5, None,    5, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, 
None, None, None, None, None,    5, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, 
None, None, None, None, None, None,    5, None,    6, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, 
None, None, None, None, None, None, None,    6, None,    8, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, 
None, None, None, None, None, None, None, None,    8, None,    8, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
   5, None, None, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None,    8, None, None, None, None, None, None, None, None,   10, None,   10, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None,   10, None, None, None, None, None, None, None, None,   10, None,    5, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None,   10, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,   10, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    7, None,    8, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,   10, None,    9, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    9, None,    9, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    9, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,   10, None,    8, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None,    7, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None,    5, None, None, None, None, None, None, None, None,    
9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    7, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None,    6, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    6, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    6, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    6, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,   10, None,    
8, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,   10, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,   10, None,   10, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,   10, None,    6, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None,    7, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    7, None,    9, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    9, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    5, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,   10, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    7, None,    9, None, None, None, None, None, None, None, None,    8, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    9, None,    9, None, None, None, None, None, None, None, None,    6, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    9, None,    7, None, None, None, None, None, None, None, None,    5, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    7, None,    6, None, None, None, None, None, None, None, None,    9, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None,    7 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    5, None,    8, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,   10, None,    9, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    9, None,   10, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,   10, None,    8, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    8, None,    7, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    7, None,   10, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,   10, None,   10 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,   10, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        clusters = [((6, 6), 3, 3), ((7, 8), 2, 2), ((4, 7), 3, 2), ((3, 3), 2, 3), ((2, 3), 2, 2), ((0, 4), 2, 2), ((1, 4), 2, 2), ((7, 7), 3, 2)]
        policyDict = { 'rateFocused' : rateFocused, 'greedy' : greedy, 'reputationFocused' : reputationFocused }
        orderInfo = \
        [(0, 78, 87, 1, 17, 29), (1, 33, 23, 2, 22, 27), (2, 14, 34, 3, 18, 31), (3, 33, 3, 4, 28, 47), (4, 89, 87, 9, 31, 44), (5, 77, 87, 10, 33, 38), (6, 58, 67, 17, 39, 54), (7, 14, 34, 18, 33, 46), (8, 77, 87, 22, 
47, 52), (9, 47, 66, 28, 49, 69), (10, 34, 43, 31, 52, 64), (11, 15, 4, 35, 60, 71), (12, 48, 49, 39, 55, 60), (13, 88, 79, 42, 67, 77), (14, 89, 97, 46, 67, 85), (15, 14, 24, 56, 78, 84), (16, 88, 98, 59, 77, 86), (17, 53, 44, 66, 81, 95), (18, 78, 88, 67, 83, 88), (19, 77, 87, 69, 84, 89), (20, 58, 88, 70, 87, 107), (21, 23, 13, 79, 97, 102), (22, 43, 42, 84, 100, 105), (23, 33, 24, 85, 106, 120), (24, 88, 58, 97, 117, 137), (25, 78, 88, 99, 119, 124), (26, 44, 32, 101, 117, 134), (27, 67, 56, 102, 125, 137), (28, 79, 69, 103, 119, 128), (29, 59, 68, 104, 124, 135), (30, 68, 66, 105, 127, 138), (31, 77, 67, 107, 128, 137), (32, 24, 33, 118, 143, 157), (33, 24, 15, 119, 143, 159), (34, 43, 35, 120, 135, 154), (35, 54, 45, 126, 141, 158), (36, 44, 33, 127, 150, 161), (37, 14, 12, 130, 152, 165), (38, 24, 35, 136, 161, 175), (39, 89, 88, 137, 154, 160), (40, 89, 79, 138, 156, 164), (41, 15, 24, 143, 161, 177), (42, 44, 52, 144, 163, 180), (43, 24, 4, 145, 160, 175), (44, 88, 78, 150, 168, 173), (45, 78, 98, 162, 177, 191), (46, 43, 52, 163, 179, 190), (47, 78, 87, 166, 181, 193), (48, 34, 33, 173, 198, 205), (49, 79, 99, 177, 201, 216), (50, 78, 68, 179, 199, 205), (51, 14, 5, 185, 210, 225), (52, 86, 85, 186, 205, 214), (53, 79, 69, 187, 207, 216), (54, 25, 26, 194, 214, 222), (55, 78, 88, 196, 213, 218), (56, 44, 43, 198, 217, 223), (57, 5, 13, 203, 228, 248), (58, 78, 76, 204, 228, 244), (59, 14, 15, 209, 230, 240), (60, 87, 89, 210, 233, 246), (61, 66, 65, 213, 233, 239), (62, 79, 69, 217, 232, 241), (63, 58, 59, 219, 234, 242), (64, 79, 87, 225, 248, 265), (65, 5, 15, 230, 245, 250), (66, 23, 3, 234, 249, 263), (67, 25, 36, 244, 265, 278), (68, 54, 45, 246, 271, 288), (69, 34, 24, 247, 267, 274), (70, 78, 88, 248, 267, 272), (71, 59, 68, 249, 272, 283), (72, 88, 68, 251, 271, 282), (73, 24, 34, 257, 280, 287), (74, 44, 53, 258, 279, 293), (75, 24, 14, 259, 283, 289), (76, 87, 89, 261, 276, 289), (77, 34, 42, 262, 280, 297), (78, 24, 
15, 269, 286, 302), (79, 68, 67, 273, 291, 297), (80, 78, 79, 277, 296, 301), (81, 86, 87, 280, 299, 308), (82, 33, 44, 283, 303, 314), (83, 33, 43, 286, 304, 309), (84, 49, 59, 292, 312, 322), (85, 88, 87, 300, 324, 331), (86, 53, 32, 303, 325, 344), (87, 34, 44, 306, 324, 330), (88, 4, 14, 310, 333, 342), (89, 14, 13, 313, 336, 343), (90, 24, 25, 316, 335, 345), (91, 78, 89, 320, 341, 352), (92, 24, 35, 324, 345, 359), (93, 23, 53, 
325, 350, 368), (94, 14, 15, 326, 346, 356), (95, 48, 46, 329, 351, 371), (96, 25, 34, 330, 349, 362), (97, 5, 13, 331, 346, 366), (98, 15, 27, 333, 350, 367), (99, 5, 6, 338, 363, 371), (100, 58, 48, 349, 366, 373), (101, 88, 99, 352, 375, 388), (102, 53, 42, 357, 378, 391)]
        driverInfo = \
        [(0, 36, 'reputationFocused', 1.0), (1, 20, 'rateFocused', 1.0), (2, 52, 'rateFocused', 1.1), (3, 70, 'reputationFocused', 1.0), (4, 83, 'greedy', 1.1), (5, 30, 'greedy', 0.9), (6, 18, 'reputationFocused', 1.0), (7, 66, 'reputationFocused', 1.1), (8, 23, 'reputationFocused', 1.0), (9, 40, 'reputationFocused', 0.9), (10, 9, 'reputationFocused', 0.9), (11, 47, 'greedy', 1.0), (12, 3, 'rateFocused', 1.0), (13, 9, 'rateFocused', 1.0), (14, 9, 'reputationFocused', 1.1)]
        orderQueue = []
        drivers = []
        # INIT ORDERS
        for id, pickup, dropoff, releaseTime, pickupTime, deliverTime in orderInfo:
            orderQueue.append(Order(id, pickup, dropoff, releaseTime, pickupTime, deliverTime, basePay))
        # INIT DRIVERS
        for id, start, policy, driverBehavior in driverInfo:
            driverPolicy = DriverPolicy(policy, policyDict[policy], random.choice([True, False]))
            drivers.append(Driver(id, start, driverPolicy, driverBehavior))

        return map, clusters, orderQueue, totalMins, drivers, basePay
#PARAMS: testNum, n, m, basePay, numDrivers, durationRange, pickupTimeRange, orderSpawnRate, 
# totalMins, dropoffThreshold=20, deliverTimeWiggleRoom=0

#print(genTest(1, 10, 10, 5, 15, (5, 10), (15, 25), .3, 360))

