from graphs import *
from ordersAndDrivers import *
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
    
    # BFS to get all available dropoffs
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


def genTest(testNum, n, m, basePay, numDrivers, durationRange, orderSpawnRate, totalMins, dropoffThreshold=12, pickupWiggleRoom=3):
    randomMap = RandomGridLayout(n, m, n * m, durationRange)
    orderCount = 0
    numNodes = n * m 
    orderQueue = []
    drivers = [(i, random.randint(0, numNodes-1)) for i in range(0, numDrivers)]
    for minute in range(totalMins):
        if random.random() < orderSpawnRate:
            pickup = random.randint(0, numNodes-1)
            dropoff = genDropoff(randomMap, pickup, dropoffThreshold)
            if dropoff == None: # could not meet threshold, exit
                 return
            orderQueue.append((orderCount, pickup, dropoff, minute))
            orderCount += 1
    testFunction = \
    f'''
# TEST {testNum}
# LAYOUT: {n}x{m} GRID
# {numDrivers} DRIVERS, {totalMins//60} HOUR PERIOD
# FLAT RATE ${basePay}/order
# EDGE DURATIONS RANGE {durationRange}
def test{testNum}():
        n = {n}
        m = {m}
        basePay = {basePay} # total price will be calculated later when assigned to driver
        totalMins = {totalMins}
        adjMatrix = \\
        {format2dList(randomMap.adjMatrix)}
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \\
        {orderQueue}
        driverInfo = \\
        {drivers}
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, pickup, dropoff, timestep in orderInfo:
            orderQueue.append(Order(id, pickup, dropoff, orderDuration, timestep, basePay))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers'''
    return testFunction

#print(genTest(8, 6, 6, 3, 10, (3, 10), .4, 360))

# TEST 1
# LAYOUT: 5x5 GRID
# 8 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $7/order
# EDGE DURATIONS RANGE (5, 30)
def test1():
    n = 5
    m = 5
    flatRate = 7
    totalMins = 360
    adjMatrix =  \
    [[None, 22, None, None, None, 24, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [22, None, 17, None, None, None, 7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [None, 17, None, 8, None, None, None, 23, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [None, None, 8, None, 19, None, None, None, 30, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [None, None, None, 19, None, None, None, None, None, 19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [24, None, None, None, None, None, 29, None, None, None, 30, None, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [None, 7, None, None, None, 29, None, 21, None, None, None, 25, None, None, None, None, None, None, None, None, None, None, None, None, None], 
    [None, None, 23, None, None, None, 21, None, 9, None, None, None, 5, None, None, None, None, None, None, None, None, None, None, None, None], 
    [None, None, None, 30, None, None, None, 9, None, 12, None, None, None, 24, None, None, None, None, None, None, None, None, None, None, None], 
    [None, None, None, None, 19, None, None, None, 12, None, None, None, None, None, 18, None, None, None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, 30, None, None, None, None, None, 22, None, None, None, 5, None, None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, 25, None, None, None, 22, None, 24, None, None, None, 6, None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, 5, None, None, None, 24, None, 29, None, None, None, 29, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None, 24, None, None, None, 29, None, 8, None, None, None, 9, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None, None, 18, None, None, None, 8, None, None, None, None, None, 15, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None, None, None, 5, None, None, None, None, None, 28, None, None, None, 26, None, None, None, None], 
    [None, None, None, None, None, None, None, None, None, None, None, 6, None, None, None, 28, None, 10, None, None, None, 29, None, None, None], 
    [None, None, None, None, None, None, None, None, None, None, None, None, 29, None, None, None, 10, None, 5, None, None, None, 9, None, None], 
    [None, None, None, None, None, None, None, None, None, None, None, None, None, 9, None, None, None, 5, None, 22, None, None, None, 23, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, 15, None, None, None, 22, None, None, None, None, None, 6], 
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 26, None, None, None, None, None, 9, None, None, None], 
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 29, None, None, None, 9, None, 10, None, None], 
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 9, None, None, None, 10, None, 6, None], 
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 23, None, None, None, 6, None, 11], 
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 6, None, None, None, 11, None]]

    map = GridLayout(n, m, n*m, adjMatrix)
    
    orderInfo = \
    [[0, 8, 16, 0], [1, 20, 9, 1], [2, 14, 11, 4], [3, 20, 2, 8], [4, 14, 23, 9], [5, 8, 15, 12], [6, 21, 7, 16], [7, 12, 6, 18], [8, 11, 12, 20], 
    [9, 11, 6, 23], [10, 1, 23, 24], [11, 15, 20, 26], [12, 0, 12, 28], [13, 13, 10, 30], [14, 15, 20, 31], [15, 9, 3, 32], [16, 2, 21, 34], 
    [17, 23, 15, 42], [18, 24, 15, 44], [19, 2, 24, 45], [20, 7, 21, 53], [21, 5, 7, 54], [22, 15, 0, 55], [23, 13, 15, 57], [24, 20, 20, 61], 
    [25, 14, 8, 62], [26, 19, 23, 68], [27, 18, 24, 76], [28, 9, 20, 78], [29, 15, 0, 81], [30, 15, 21, 86], [31, 18, 6, 89], [32, 6, 7, 90], 
    [33, 15, 11, 91], [34, 17, 13, 98], [35, 8, 10, 108], [36, 2, 2, 109], [37, 12, 17, 111], [38, 19, 8, 116], [39, 18, 17, 120], [40, 3, 10, 121], 
    [41, 21, 7, 122], [42, 10, 23, 124], [43, 15, 8, 125], [44, 13, 16, 126], [45, 0, 14, 132], [46, 1, 12, 133], [47, 8, 24, 135], [48, 3, 14, 137], 
    [49, 17, 13, 140], [50, 2, 24, 141], [51, 19, 6, 145], [52, 21, 7, 146], [53, 18, 7, 151], [54, 12, 3, 156], [55, 16, 13, 161], [56, 15, 13, 162], 
    [57, 17, 1, 163], [58, 5, 21, 164], [59, 3, 15, 165], [60, 1, 6, 166], [61, 22, 17, 168], [62, 12, 17, 169], [63, 3, 24, 171], [64, 8, 12, 172], 
    [65, 23, 15, 174], [66, 18, 0, 177], [67, 21, 23, 178], [68, 11, 6, 179], [69, 1, 13, 180], [70, 4, 15, 182], [71, 12, 8, 183], [72, 0, 18, 185], 
    [73, 19, 4, 190], [74, 20, 10, 191], [75, 24, 16, 194], [76, 2, 10, 195], [77, 17, 14, 196], [78, 7, 22, 198], [79, 21, 13, 199], [80, 17, 2, 200], 
    [81, 16, 0, 202], [82, 4, 10, 204], [83, 16, 11, 205], [84, 3, 12, 207], [85, 8, 24, 208], [86, 23, 22, 209], [87, 10, 19, 211], [88, 8, 19, 212], 
    [89, 20, 1, 213], [90, 15, 18, 214], [91, 15, 12, 215], [92, 16, 3, 226], [93, 3, 9, 228], [94, 22, 24, 235], [95, 3, 0, 237], [96, 5, 13, 240], 
    [97, 12, 13, 242], [98, 8, 8, 243], [99, 20, 5, 244], [100, 9, 6, 245], [101, 22, 5, 246], [102, 8, 15, 247], [103, 15, 24, 248], [104, 2, 3, 249],
    [105, 12, 2, 254], [106, 3, 16, 255], [107, 8, 9, 256], [108, 15, 3, 260], [109, 2, 19, 261], [110, 24, 15, 263], [111, 5, 18, 271], [112, 22, 16, 275], 
    [113, 4, 2, 280], [114, 0, 7, 282], [115, 21, 19, 284], [116, 21, 3, 289], [117, 22, 17, 295], [118, 6, 18, 304], [119, 17, 24, 305], [120, 23, 13, 307], 
    [121, 22, 6, 311], [122, 20, 22, 314], [123, 21, 6, 318], [124, 16, 19, 319], [125, 10, 24, 320], [126, 22, 3, 323], [127, 17, 13, 327], [128, 6, 18, 330], 
    [129, 13, 6, 331], [130, 7, 18, 332], [131, 12, 4, 333], [132, 2, 1, 335], [133, 3, 19, 339], [134, 11, 15, 340], [135, 21, 2, 349], [136, 14, 7, 350], 
    [137, 18, 24, 355], [138, 0, 21, 359]]
    
    driverInfo = \
    [[0, 13],
    [1, 8],
    [2, 18],
    [3, 23],
    [4, 21],
    [5, 14],
    [6, 24],
    [7, 3]]

    orderQueue = []
    drivers = []
    orderDuration = 0 # will update when assigned to driver
    # INIT ORDERS
    for id, start, dropoff, timestep in orderInfo:
        orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
    # INIT DRIVERS
    for id, start in driverInfo:
        drivers.append(Driver(id, start))

    return map, orderQueue, totalMins, drivers

# TEST 2
# LAYOUT: 6x6 GRID
# 9 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $7/order
# EDGE DURATIONS RANGE (3, 10)
def test2():
    n = 6
    m = 6
    totalMins = 360
    flatRate = 7
    adjMatrix = \
[
 [ None, 7, None, None, None, None,7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    7, None,    9, None, None, None, None, 8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    9, None,    4, None, None, None, None, 4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    4, None,   10, None, None, None, None, 4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,   10, None,    8, None, None, None, None, 10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    8, None, None, None, None, None, None,  8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    7, None, None, None, None, None, None,    3, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    8, None, None, None, None,    3, None,    7, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    4, None, None, None, None,    7, None,    6, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    4, None, None, None, None,    6, None,    9, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,   10, None, None, None, None,    9, None,   10, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    8, None, None, None, None,   10, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    9, None, None, None, None, None, None,    9, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    9, None, None, None, None,    9, None,    7, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    4, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    3, None, None, None, None,    4, None,    7, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    7, None,    3, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None,    3, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None,    7, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None,    7, None,    9, None, None, None, None,    5, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    9, None,    3, None, None, None, None,    8, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None,    3, None,    5, None, None, None, None,    8, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None,    5, None, None, None, None, None, None,   10, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None,    5, None, None, None, None,    8, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None,    5, None,    4, None, None, None, None,   10, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None,    4, None,    3, None, None, None, None,    8, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    3, None,    5, None, None, None, None,    8, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    5, None,    3, None, None, None, None,    6, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None, None, None, None, None, None,    3 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    3, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None,    7, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    4, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    4, None,    3, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    3, None,    3 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None,    3, None ]
]
    driverInfo =  \
    [(0, 8), (1, 11), (2, 16), (3, 33), (4, 33), (5, 9), (6, 20), (7, 12), (8, 23)]
    orderInfo =  \
    [(0, 33, 17, 0, 0, 7), (1, 6, 25, 0, 2, 7), (2, 23, 14, 0, 4, 7), (3, 11, 4, 0, 5, 7), 
     (4, 10, 30, 0, 6, 7), (5, 28, 34, 0, 7, 7), (6, 11, 4, 0, 10, 7), (7, 33, 24, 0, 11, 7),
       (8, 22, 13, 0, 13, 7), (9, 32, 22, 0, 17, 7), (10, 14, 25, 0, 22, 7), (11, 18, 0, 0, 27, 7), 
       (12, 17, 6, 0, 29, 7), (13, 35, 8, 0, 30, 7), (14, 2, 17, 0, 33, 7), (15, 26, 31, 0, 39, 7), 
       (16, 28, 8, 0, 41, 7), (17, 18, 12, 0, 43, 7), (18, 7, 19, 0, 45, 7), (19, 2, 1, 0, 51, 7), 
       (20, 6, 1, 0, 54, 7), (21, 11, 28, 0, 55, 7), (22, 0, 26, 0, 56, 7), (23, 12, 33, 0, 60, 7), 
       (24, 15, 4, 0, 66, 7), (25, 23, 34, 0, 71, 7), (26, 6, 15, 0, 73, 7), (27, 10, 23, 0, 77, 7), 
       (28, 13, 3, 0, 78, 7), (29, 33, 7, 0, 79, 7), (30, 15, 18, 0, 81, 7), (31, 25, 4, 0, 82, 7),
         (32, 29, 1, 0, 84, 7), (33, 34, 32, 0, 85, 7), (34, 6, 29, 0, 89, 7), (35, 10, 16, 0, 91, 7), 
         (36, 22, 7, 0, 93, 7), (37, 10, 25, 0, 96, 7), (38, 13, 1, 0, 97, 7), (39, 20, 16, 0, 98, 7), 
         (40, 31, 5, 0, 99, 7), (41, 7, 7, 0, 102, 7), (42, 2, 24, 0, 104, 7), (43, 12, 13, 0, 105, 7), 
         (44, 3, 4, 0, 109, 7), (45, 10, 8, 0, 110, 7), (46, 16, 25, 0, 115, 7), (47, 18, 1, 0, 116, 7), 
         (48, 6, 6, 0, 124, 7), (49, 27, 23, 0, 125, 7), (50, 8, 30, 0, 128, 7), (51, 35, 25, 0, 129, 7), 
         (52, 28, 18, 0, 132, 7), (53, 25, 32, 0, 134, 7), (54, 15, 21, 0, 139, 7), (55, 18, 18, 0, 140, 7), 
         (56, 7, 4, 0, 144, 7), (57, 10, 1, 0, 145, 7), (58, 6, 27, 0, 146, 7), (59, 7, 12, 0, 148, 7), 
         (60, 14, 10, 0, 151, 7), (61, 8, 9, 0, 158, 7), (62, 11, 3, 0, 159, 7), (63, 11, 33, 0, 166, 7), 
         (64, 32, 7, 0, 169, 7), (65, 30, 2, 0, 172, 7), (66, 23, 25, 0, 173, 7), (67, 7, 32, 0, 174, 7), 
         (68, 11, 18, 0, 175, 7), (69, 7, 9, 0, 176, 7), (70, 5, 8, 0, 181, 7), (71, 25, 24, 0, 182, 7), (72, 20, 31, 0, 186, 7), 
         (73, 3, 22, 0, 187, 7), (74, 26, 25, 0, 189, 7), (75, 33, 35, 0, 190, 7), (76, 17, 6, 0, 191, 7), 
         (77, 5, 27, 0, 196, 7), (78, 16, 32, 0, 197, 7), (79, 30, 5, 0, 199, 7), (80, 26, 19, 0, 200, 7), (81, 0, 25, 0, 201, 7), 
         (82, 29, 10, 0, 204, 7), (83, 28, 0, 0, 206, 7), (84, 10, 10, 0, 208, 7), (85, 29, 23, 0, 209, 7), (86, 28, 6, 0, 217, 7), 
         (87, 7, 18, 0, 220, 7), (88, 4, 33, 0, 226, 7), (89, 4, 33, 0, 227, 7), (90, 13, 1, 0, 235, 7), (91, 7, 1, 0, 236, 7), (92, 30, 16, 0, 239, 7),
        (93, 29, 29, 0, 243, 7), (94, 33, 28, 0, 245, 7), (95, 4, 14, 0, 246, 7), (96, 17, 24, 0, 247, 7), (97, 0, 30, 0, 252, 7),
        (98, 11, 1, 0, 253, 7), (99, 22, 27, 0, 254, 7), (100, 21, 22, 0, 256, 7), (101, 19, 28, 0, 258, 7), (102, 29, 7, 0, 259, 7), (103, 20, 5, 0, 260, 7), (104, 16, 17, 0, 262, 7), (105, 3, 13, 0, 266, 7), (106, 3, 31, 0, 267, 7), (107, 8, 2, 0, 268, 7), (108, 16, 24, 0, 272, 7), (109, 21, 12, 0, 279, 7), (110, 32, 35, 0, 282, 7), (111, 30, 16, 0, 287, 7), (112, 14, 28, 0, 290, 7), (113, 19, 32, 0, 292, 7), (114, 19, 21, 0, 299, 7), (115, 16, 15, 0, 301, 7), (116, 29, 26, 0, 302, 7), (117, 7, 6, 0, 307, 7), (118, 0, 15, 0, 310, 7), (119, 4, 24, 0, 311, 7), (120, 22, 16, 0, 312, 7), (121, 14, 30, 0, 320, 7), (122, 27, 26, 0, 321, 7), (123, 29, 0, 0, 323, 7), (124, 27, 18, 0, 327, 7), (125, 0, 34, 0, 330, 7), (126, 9, 14, 0, 331, 7), (127, 24, 34, 0, 336, 7), (128, 33, 27, 0, 339, 7), (129, 12, 4, 0, 341, 7), (130, 17, 14, 0, 342, 7), (131, 14, 25, 0, 344, 7), (132, 23, 5, 0, 346, 7), (133, 8, 1, 0, 349, 7), 
        (134, 4, 3, 0, 351, 7), (135, 5, 10, 0, 352, 7), (136, 13, 13, 0, 354, 7), (137, 23, 28, 0, 356, 7)]
    
    map = GridLayout(n, m, n*m, adjMatrix)
    orderQueue = []
    drivers = []
    orderDuration = 0 # will update when assigned to driver
    # INIT ORDERS
    for id, start, dropoff, orderDuration, timestep, flatRate in orderInfo:
        orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
    # INIT DRIVERS
    for id, start in driverInfo:
        drivers.append(Driver(id, start))

    return map, orderQueue, totalMins, drivers

# TEST 3
# LAYOUT: 8x8 GRID
# 10 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $7/order
# EDGE DURATIONS RANGE (3, 10)
def test3():
        n = 8
        m = 8
        flatRate = 7
        totalMins = 360
        adjMatrix = \
        [
 [ None,    7, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    7, None,    3, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    3, None,    4, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    4, None,    9, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    9, None,    8, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    8, None,   10, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,   10, None,    8, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    6, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,   10, None, None, None, None, None, None,    4, None,    8, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    5, None, None, None, None, None, None,    8, None,    6, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    8, None, None, None, None, None, None,    6, None,    4, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    3, None, None, None, None, None, None,    4, None,    5, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,   10, None, None, None, None, None, None,    5, None,   10, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    7, None, None, None, None, None, None,   10, None,    5, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    7, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    4, None,   10, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,   10, None,    5, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    5, None,    4, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    4, None,    5, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    5, None,    3, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    3, None,    4, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None,    8, None,    8, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,   10, None,    4, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    4, None,   10, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None,   10, None,    6, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    6, None,    3, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None,    3, None,    8, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    8, None,    6, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    6, None,    8, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None,   10, None,    8, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    8, None,    5, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    5, None,    3, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    3, None,    6, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None,    6, None,    4, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    4, None,    4, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    4, None,    6, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None,    6, None,    6, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None,    3, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None,    6, None,    8, None, None, None, None, None, None,    5, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,    8, None,    4, None, None, None, None, None, None,   10, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None,    4, None,    4, None, None, None, None, None, None,    4, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    4, None,    5, None, None, None, None, None, None,    3, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,    5, None,    9, None, None, None, None, None, None,    6, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,    9, None,    3, None, None, None, None, None, None,    8, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    8 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None,    5, None,   10, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None,   10, None,    4, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None,    4, None,    6, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,    6, None,    3, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None,    3, None,    6, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    6, None,    9 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    9, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \
        [(0, 44, 58, 0, 0, 7), (1, 50, 21, 0, 4, 7), (2, 34, 56, 0, 5, 7), (3, 34, 15, 0, 11, 7), (4, 18, 45, 0, 12, 7), (5, 28, 42, 0, 15, 7), (6, 10, 18, 0, 16, 7), (7, 7, 18, 0, 17, 7), (8, 19, 30, 0, 20, 7), (9, 50, 29, 0, 28, 7), (10, 9, 50, 0, 29, 7), (11, 24, 32, 0, 30, 7), (12, 23, 21, 0, 34, 7), (13, 39, 45, 0, 36, 7), (14, 42, 38, 0, 37, 7), (15, 2, 35, 0, 40, 7), (16, 19, 46, 0, 41, 7), (17, 16, 32, 0, 42, 7), (18, 12, 24, 0, 45, 7), (19, 11, 7, 0, 50, 7), (20, 40, 29, 0, 52, 7), (21, 57, 25, 0, 53, 7), (22, 45, 62, 0, 54, 7), (23, 5, 8, 0, 55, 7), (24, 31, 16, 0, 56, 7), (25, 54, 40, 0, 58, 7), (26, 60, 57, 0, 61, 7), (27, 1, 57, 0, 62, 7), (28, 28, 48, 0, 63, 7), (29, 26, 7, 0, 65, 7), (30, 10, 33, 0, 70, 7), (31, 59, 40, 0, 72, 7), (32, 11, 31, 0, 75, 7), (33, 24, 49, 0, 77, 7), (34, 35, 59, 0, 82, 7), (35, 21, 31, 0, 83, 7), (36, 18, 11, 0, 87, 7), (37, 27, 31, 0, 89, 7), (38, 39, 38, 0, 96, 7), (39, 19, 40, 0, 97, 7), (40, 57, 9, 0, 103, 7), (41, 33, 36, 0, 106, 7), (42, 62, 21, 0, 107, 7), (43, 46, 39, 0, 108, 7), (44, 54, 16, 0, 109, 7), (45, 22, 55, 0, 114, 7), (46, 38, 33, 0, 115, 7), (47, 50, 49, 0, 117, 7), (48, 43, 20, 0, 118, 7), (49, 31, 5, 0, 122, 7), (50, 24, 52, 0, 125, 7), (51, 27, 51, 0, 128, 7), (52, 31, 2, 0, 129, 7), (53, 52, 43, 0, 131, 7), (54, 53, 31, 0, 135, 7), (55, 17, 19, 0, 138, 7), (56, 9, 32, 0, 140, 7), (57, 40, 26, 0, 142, 7), (58, 18, 36, 0, 143, 7), (59, 18, 20, 0, 144, 7), (60, 13, 13, 0, 145, 7), (61, 21, 20, 0, 147, 7), (62, 50, 17, 0, 149, 7), (63, 10, 34, 0, 151, 7), (64, 2, 61, 0, 152, 7), (65, 34, 9, 0, 156, 7), (66, 46, 9, 0, 157, 7), (67, 60, 20, 0, 160, 7), (68, 6, 7, 0, 162, 7), (69, 40, 23, 0, 163, 7), (70, 31, 10, 0, 164, 7), (71, 24, 37, 0, 165, 7), (72, 5, 13, 0, 166, 7), (73, 9, 55, 0, 168, 7), (74, 34, 35, 0, 170, 7), (75, 63, 14, 0, 172, 7), (76, 14, 30, 0, 178, 7), (77, 44, 28, 0, 179, 7), (78, 24, 38, 0, 181, 7), (79, 39, 34, 0, 182, 7), (80, 5, 31, 0, 187, 7), (81, 53, 53, 0, 189, 7), (82, 57, 41, 0, 190, 7), (83, 0, 44, 0, 192, 7), (84, 61, 27, 0, 194, 7), (85, 56, 15, 0, 195, 7), (86, 30, 59, 0, 199, 7), (87, 44, 8, 0, 200, 7), (88, 51, 46, 0, 203, 7), (89, 58, 2, 0, 205, 7), (90, 8, 25, 0, 209, 7), (91, 37, 30, 0, 210, 7), (92, 52, 51, 0, 212, 7), (93, 45, 44, 0, 217, 7), (94, 39, 12, 0, 220, 7), (95, 3, 58, 0, 227, 7), (96, 11, 38, 0, 228, 7), (97, 17, 44, 0, 230, 7), (98, 4, 54, 0, 232, 7), (99, 56, 16, 0, 233, 7), (100, 49, 43, 0, 235, 7), (101, 10, 9, 0, 236, 7), (102, 18, 63, 0, 239, 7), (103, 44, 48, 0, 241, 7), (104, 35, 56, 0, 243, 7), (105, 38, 0, 0, 244, 7), (106, 62, 22, 0, 250, 7), (107, 41, 35, 0, 251, 7), (108, 35, 46, 0, 252, 7), (109, 6, 61, 0, 254, 7), (110, 63, 53, 0, 257, 7), (111, 27, 38, 0, 258, 7), (112, 40, 50, 0, 259, 7), (113, 13, 8, 0, 260, 7), (114, 39, 59, 0, 262, 7), (115, 20, 33, 0, 264, 7), (116, 25, 14, 0, 267, 7), (117, 12, 12, 0, 268, 7), (118, 29, 22, 0, 275, 7), (119, 54, 38, 0, 276, 7), (120, 4, 21, 0, 277, 7), (121, 51, 29, 0, 278, 7), (122, 14, 25, 0, 279, 7), (123, 32, 63, 0, 280, 7), (124, 50, 6, 0, 285, 7), (125, 59, 39, 0, 287, 7), (126, 2, 24, 0, 288, 7), (127, 23, 25, 0, 289, 7), (128, 50, 20, 0, 293, 7), (129, 45, 58, 0, 294, 7), (130, 11, 59, 0, 297, 7), (131, 3, 9, 0, 298, 7), (132, 9, 5, 0, 300, 7), (133, 42, 11, 0, 303, 7), (134, 9, 62, 0, 307, 7), (135, 2, 44, 0, 308, 7), (136, 25, 32, 0, 309, 7), (137, 24, 40, 0, 311, 7), (138, 60, 33, 0, 314, 7), (139, 48, 52, 0, 315, 7), (140, 41, 44, 0, 316, 7), (141, 14, 21, 0, 322, 7), (142, 28, 32, 0, 323, 7), (143, 24, 44, 0, 326, 7), (144, 6, 13, 0, 328, 7), (145, 18, 13, 0, 333, 7), (146, 29, 54, 0, 338, 7), (147, 8, 49, 0, 340, 7), (148, 59, 26, 0, 342, 7), (149, 1, 47, 0, 345, 7), (150, 45, 25, 0, 347, 7), (151, 59, 43, 0, 349, 7), (152, 58, 30, 0, 350, 7), (153, 36, 63, 0, 352, 7), (154, 29, 54, 0, 353, 7), (155, 16, 63, 0, 354, 7), (156, 29, 15, 0, 357, 7)]
        driverInfo = \
        [(0, 34), (1, 1), (2, 28), (3, 41), (4, 40), (5, 18), (6, 2), (7, 43), (8, 46), (9, 16)]
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, start, dropoff, orderDuration, timestep, flatRate in orderInfo:
            orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers

# TEST 4
# LAYOUT: 3x3 GRID
# 4 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $7/hour
# EDGE DURATION RANGE (3, 10)
def test4():
        n = 3
        m = 3
        flatRate = 7
        totalMins = 360
        adjMatrix = \
        [
 [ None,   10, None,    7, None, None, None, None, None ],
 [   10, None,    8, None,    8, None, None, None, None ],
 [ None,    8, None, None, None,    5, None, None, None ],
 [    7, None, None, None,    6, None,    4, None, None ],
 [ None,    8, None,    6, None,    7, None,    3, None ],
 [ None, None,    5, None,    7, None, None, None,    5 ],
 [ None, None, None,    4, None, None, None,    5, None ],
 [ None, None, None, None,    3, None,    5, None,    8 ],
 [ None, None, None, None, None,    5, None,    8, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \
        [(0, 0, 4, 0, 7), (1, 7, 8, 5, 7), (2, 3, 8, 8, 7), (3, 3, 7, 11, 7), (4, 5, 8, 16, 7), (5, 5, 2, 18, 7), (6, 7, 4, 19, 7), (7, 8, 0, 20, 7), (8, 3, 4, 22, 7), (9, 4, 1, 25, 7), (10, 0, 5, 26, 7), (11, 3, 5, 27, 7), (12, 5, 5, 33, 7), (13, 2, 4, 34, 7), (14, 5, 1, 35, 7), (15, 0, 0, 38, 7), (16, 2, 3, 42, 7), (17, 5, 0, 43, 7), (18, 6, 6, 44, 7), (19, 5, 5, 50, 7), (20, 8, 0, 52, 7), (21, 5, 3, 53, 7), (22, 3, 1, 55, 7), (23, 2, 0, 57, 7), (24, 4, 0, 60, 7), (25, 4, 5, 63, 7), (26, 0, 6, 64, 7), (27, 4, 0, 65, 7), (28, 1, 3, 66, 7), (29, 8, 3, 68, 7), (30, 0, 4, 72, 7), (31, 8, 4, 73, 7), (32, 0, 6, 75, 7), (33, 3, 3, 78, 7), (34, 0, 2, 79, 7), (35, 5, 4, 82, 7), (36, 6, 2, 83, 7), (37, 5, 2, 84, 7), (38, 2, 8, 91, 7), (39, 6, 8, 94, 7), (40, 6, 7, 95, 7), (41, 7, 8, 99, 7), (42, 4, 7, 101, 7), (43, 6, 4, 102, 7), (44, 7, 3, 103, 7), (45, 0, 1, 104, 7), (46, 5, 7, 105, 7), (47, 7, 7, 109, 7), (48, 0, 8, 110, 7), (49, 6, 4, 116, 7), (50, 1, 7, 117, 7), (51, 0, 1, 119, 7), (52, 6, 3, 121, 7), (53, 4, 5, 124, 7), (54, 0, 5, 130, 7), (55, 2, 2, 132, 7), (56, 4, 6, 139, 7), (57, 4, 6, 140, 7), (58, 0, 6, 144, 7), (59, 5, 2, 147, 7), (60, 3, 4, 148, 7), (61, 3, 1, 149, 7), (62, 7, 5, 152, 7), (63, 0, 0, 153, 7), (64, 2, 5, 154, 7), (65, 6, 6, 155, 7), (66, 6, 2, 157, 7), (67, 2, 7, 158, 7), (68, 2, 3, 161, 7), (69, 7, 8, 162, 7), (70, 5, 4, 164, 7), (71, 0, 5, 166, 7), (72, 5, 0, 170, 7), (73, 5, 1, 174, 7), (74, 3, 5, 175, 7), (75, 3, 5, 176, 7), (76, 5, 2, 181, 7), (77, 0, 4, 183, 7), (78, 0, 2, 184, 7), (79, 1, 2, 188, 7), (80, 1, 2, 190, 7), (81, 8, 3, 193, 7), (82, 1, 6, 194, 7), (83, 2, 0, 198, 7), (84, 5, 5, 199, 7), (85, 8, 6, 201, 7), (86, 8, 1, 202, 7), (87, 4, 3, 205, 7), (88, 5, 5, 208, 7), (89, 4, 1, 210, 7), (90, 1, 0, 212, 7), (91, 5, 6, 214, 7), (92, 4, 7, 216, 7), (93, 1, 1, 218, 7), (94, 0, 2, 219, 7), (95, 3, 1, 221, 7), (96, 8, 4, 223, 7), (97, 1, 4, 226, 7), (98, 2, 8, 229, 7), (99, 0, 1, 233, 7), (100, 2, 3, 237, 7), (101, 0, 4, 241, 7), (102, 8, 1, 243, 7), (103, 1, 8, 247, 7), (104, 2, 4, 250, 7), (105, 8, 6, 251, 7), (106, 2, 5, 254, 7), (107, 8, 1, 255, 7), (108, 3, 2, 256, 7), (109, 0, 8, 258, 7), (110, 1, 1, 259, 7), (111, 0, 8, 260, 7), (112, 3, 1, 261, 7), (113, 4, 3, 263, 7), (114, 4, 2, 264, 7), (115, 6, 7, 268, 7), (116, 6, 4, 271, 7), (117, 8, 8, 274, 7), (118, 3, 0, 277, 7), (119, 2, 5, 278, 7), (120, 6, 4, 279, 7), (121, 8, 0, 286, 7), (122, 1, 0, 289, 7), (123, 8, 8, 290, 7), (124, 4, 6, 291, 7), (125, 1, 4, 293, 7), (126, 2, 1, 294, 7), (127, 3, 1, 295, 7), (128, 8, 7, 296, 7), (129, 1, 0, 300, 7), (130, 5, 6, 302, 7), (131, 6, 8, 303, 7), (132, 1, 1, 304, 7), (133, 2, 1, 308, 7), (134, 1, 5, 312, 7), (135, 5, 6, 315, 7), (136, 5, 1, 322, 7), (137, 2, 1, 327, 7), (138, 0, 6, 329, 7), (139, 5, 2, 331, 7), (140, 8, 1, 332, 7), (141, 1, 5, 333, 7), (142, 7, 4, 336, 7), (143, 4, 1, 338, 7), (144, 5, 1, 340, 7), (145, 8, 6, 341, 7), (146, 3, 1, 342, 7), (147, 1, 7, 344, 7), (148, 0, 2, 345, 7), (149, 4, 1, 346, 7), (150, 0, 1, 347, 7), (151, 0, 7, 351, 7), (152, 8, 8, 353, 7), (153, 7, 8, 357, 7), (154, 5, 6, 358, 7)]
        driverInfo = \
        [(0, 7), (1, 7), (2, 7), (3, 6)]
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, start, dropoff, timestep, flatRate in orderInfo:
            orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers

# TEST 5
# LAYOUT: 10x10 GRID
# 15 DRIVERS, 6 HOUR PERIOD   
# FLAT RATE $7/order
# EDGE DURATIONS RANGE (3, 10)
def test5():
        n = 10
        m = 10
        flatRate = 7
        totalMins = 360
        adjMatrix = \
        [
 [ None,   10, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [   10, None,    5, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    5, None,    7, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    7, None,    4, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    4, None,    4, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    4, None,    3, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    3, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    9, None,    6, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    6, None,    3, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    3, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,   10, None, None, None, None, None, None, None, None,    9, None,    4, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    7, None, None, None, None, None, None, None, None,    4, None,    3, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    3, None, None, None, None, None, None, None, None,    3, None,   10, None, None, None, None, None, None, None, None,   
 9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    8, None, None, None, None, None, None, None, None,   10, None,    8, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    8, None,    7, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    7, None,    4, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    4, None,    9, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None,    5, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    3, None,   10, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,   10, None,   
 9, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None,    8, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,   
 8, None,    8, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    8, None,    8, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    8, None,    4, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    4, None,    4, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    4, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    4, None,    8, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    8, None,    3, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   
 3, None, None, None, None, None, None, None, None,    3, None,    4, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    4, None,    9, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    9, None,    3, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    3, None,    4, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    4, None,    8, None, None, None, None, None, None, None, None,  
  4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    8, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,   10, None,    6, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None,    4, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    4, None,    8, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    8, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    7, None,    7, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    7, None,  
  8, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    8, None,    3, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,  
  3, None,    3, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    7, None,    3, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    3, None,    5, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    8, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    8, None,    5, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    5, None,    4, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    4, None,    4, None, None, None, None, None, None, None, None,   10, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  
  8, None, None, None, None, None, None, None, None,    4, None,   10, None, None, None, None, None, None, None, None,   10, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,   10, None,   10, None, None, None, None, None, None, None, None,    9, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None,    9, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,   10, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    9, None,    8, None, None, None, None, None, None, None, None, 
   4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    8, None,    5, None, None, None, None, None, None, None, 
None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    7, None, None, None, None, None, None, 
None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    7, None,    5, None, None, None, None, None, 
None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    5, None,    8, None, None, None, None, 
None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    8, None,    5, None, None, None, 
None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    5, None,    8, None, None, 
None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    8, None,    5, None, 
None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None, None, 
None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, 
   5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    5, 
None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, 
   7, None,    6, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, 
None,    6, None,    9, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, 
None, None,    9, None,    9, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, 
None, None, None,    9, None,    4, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, 
None, None, None, None,    4, None,    6, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, 
None, None, None, None, None,    6, None,   10, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, 
None, None, None, None, None, None,   10, None,    7, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, 
None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, 
None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
   8, None, None, None, None, None, None, None, None,    5, None,    3, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None,    8, None, None, None, None, None, None, None, None,    3, None,    3, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None,    6, None, None, None, None, None, None, None, None,    3, None,    4, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None,    6, None, None, None, None, None, None, None, None,    4, None,    9, None, None, None, None, None, None, None, None,    5, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None,    5, None, None, None, None, None, None, None, None,    9, None,    3, None, None, None, None, None, None, None, None,    4, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    3, None,    6, None, None, None, None, None, None, None, None,    3, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    6, None,    5, None, None, None, None, None, None, None, None,   10, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None,    5, None, None, None, None, None, None, None, None,    5, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    3 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    5, None,    8, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    8, None,    8, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    8, None,    6, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None,    6, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    6, None,    9, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    9, None,    8, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    8, None,    5, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    5, None,    3 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    3, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \
        [(0, 35, 27, 3), (1, 74, 91, 10), (2, 67, 90, 12), (3, 12, 79, 14), (4, 24, 57, 17), (5, 96, 61, 22), (6, 91, 37, 23), (7, 56, 93, 28), (8, 41, 44, 29), (9, 28, 77, 30), (10, 69, 68, 35), (11, 18, 93, 38), (12, 71, 73, 42), (13, 97, 78, 46), (14, 95, 39, 47), (15, 47, 62, 49), 
(16, 53, 79, 53), (17, 51, 48, 54), (18, 4, 43, 57), (19, 98, 29, 63), (20, 86, 17, 65), (21, 33, 78, 70), (22, 13, 33, 71), (23, 21, 13, 74), 
(24, 81, 84, 76), (25, 33, 27, 77), (26, 69, 22, 78), (27, 21, 92, 79), (28, 59, 42, 80), (29, 46, 85, 81), (30, 38, 58, 84), (31, 21, 23, 88), (32, 95, 91, 91), (33, 24, 97, 96), (34, 78, 79, 98), (35, 84, 33, 99), (36, 84, 3, 100), (37, 92, 3, 105), (38, 87, 78, 106), (39, 11, 41, 111), (40, 49, 66, 113), (41, 91, 24, 115), (42, 8, 55, 119), (43, 83, 92, 121), (44, 66, 64, 129), (45, 31, 79, 130), (46, 20, 29, 131), (47, 67, 7, 132), (48, 78, 5, 133), (49, 50, 82, 134), (50, 98, 59, 139), (51, 59, 9, 140), (52, 57, 17, 143), (53, 16, 38, 151), (54, 26, 22, 154), (55, 74, 40, 156), (56, 81, 49, 158), (57, 96, 47, 159), (58, 41, 54, 160), (59, 96, 3, 162), (60, 84, 15, 165), (61, 27, 72, 167), (62, 82, 39, 168), (63, 33, 84, 170), (64, 41, 12, 171), (65, 63, 96, 172), (66, 28, 62, 174), (67, 43, 44, 175), (68, 98, 90, 178), (69, 80, 89, 179), (70, 10, 34, 184), (71, 96, 12, 189), (72, 47, 23, 192), (73, 80, 49, 194), (74, 8, 79, 198), (75, 77, 89, 199), (76, 77, 52, 200), (77, 17, 99, 201), (78, 74, 75, 202), (79, 15, 99, 207), (80, 82, 2, 208), (81, 3, 5, 211), (82, 32, 19, 214), (83, 35, 55, 216), (84, 45, 9, 217), (85, 82, 
24, 218), (86, 10, 13, 221), (87, 46, 58, 228), (88, 64, 58, 229), (89, 36, 67, 232), (90, 78, 27, 233), (91, 19, 99, 234), (92, 27, 79, 239), 
(93, 59, 68, 240), (94, 97, 43, 241), (95, 68, 95, 242), (96, 19, 33, 243), (97, 59, 60, 244), (98, 49, 71, 247), (99, 8, 99, 249), (100, 84, 49, 251), (101, 51, 66, 252), (102, 71, 95, 256), (103, 11, 26, 258), (104, 1, 62, 259), (105, 79, 52, 263), (106, 64, 24, 264), (107, 55, 74, 267), (108, 81, 21, 268), (109, 16, 52, 272), (110, 65, 10, 275), (111, 2, 90, 276), (112, 26, 71, 285), (113, 91, 80, 286), (114, 55, 18, 288), (115, 2, 57, 289), (116, 85, 85, 290), (117, 8, 59, 291), (118, 46, 41, 293), (119, 77, 16, 297), (120, 84, 72, 302), (121, 29, 43, 307), (122, 42, 10, 308), (123, 77, 13, 311), (124, 46, 13, 312), (125, 79, 36, 313), (126, 14, 0, 314), (127, 81, 42, 316), (128, 51, 24, 317), (129, 22, 77, 323), (130, 86, 47, 324), (131, 38, 76, 326), (132, 97, 94, 327), (133, 69, 58, 328), (134, 91, 94, 330), (135, 81, 47, 336), (136, 19, 89, 341), (137, 28, 98, 342), (138, 98, 54, 343), (139, 8, 34, 347), (140, 82, 64, 350), (141, 39, 43, 351), (142, 18, 63, 356), (143, 47, 14, 358)]
        driverInfo = \
        [(0, 84), (1, 37), (2, 99), (3, 98), (4, 9), (5, 17), (6, 71), (7, 35), (8, 58), (9, 8), (10, 81), (11, 49), (12, 21), (13, 90), (14, 25)]
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, start, dropoff, timestep in orderInfo:
            orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers


##############################################################
################## TESTS WITH ORDER QUADRANTS ################
##############################################################

# TEST 6
# LAYOUT: 10x10 GRID
# 15 DRIVERS, 6 HOUR PERIOD   
# FLAT RATE $7/order
# EDGE DURATIONS RANGE (3, 10)
def test6():
        n = 10
        m = 10
        flatRate = 7
        totalMins = 360
        adjMatrix = \
        [
 [ None,   10, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [   10, None,    5, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    5, None,    9, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    9, None,    7, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    7, None,    8, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    8, None,    4, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    4, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    5, None,    4, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    4, None,    5, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    6, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,   10, None, None, None, None, None, None, None, None,    7, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    5, None, None, None, None, None, None, None, None,   10, None,    3, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    4, None, None, None, None, None, None, None, None,    3, None,    5, None, None, None, None, None, None, None, None,   
 3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    3, None, None, None, None, None, None, None, None,    5, None,    4, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    4, None,    5, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    5, None,    4, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    4, None,    4, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    4, None,    8, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    3, None,    9, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    9, None,   
10, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,   10, None,    6, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,   
 6, None,    3, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    3, None,    3, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    3, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,   10, None,    5, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    5, None,    4, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,   10, None,    8, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   
 9, None, None, None, None, None, None, None, None,   10, None,    3, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    3, None,    5, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    5, None,    3, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    3, None,    5, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    5, None,    9, None, None, None, None, None, None, None, None,  
 10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    9, None,    8, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    5, None,    6, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    6, None,    8, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    8, None,    8, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    8, None,   10, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,   10, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    7, None,  
  4, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    4, None,    4, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,  
  4, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    3, None,    9, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    9, None,    4, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,    4, None,    9, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    9, None,   10, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,   10, None,    5, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    5, None,    7, None, None, None, None, None, None, None, None,    8, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  
  5, None, None, None, None, None, None, None, None,    7, None,   10, None, None, None, None, None, None, None, None,    7, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,   10, None,    9, None, None, None, None, None, None, None, None,    9, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None,    6, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    3, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    7, None,    9, None, None, None, None, None, None, None, None, 
   9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    9, None,    3, None, None, None, None, None, None, None, 
None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    3, None,    5, None, None, None, None, None, None, 
None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    5, None,    9, None, None, None, None, None, 
None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    9, None,    5, None, None, None, None, 
None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    5, None,    7, None, None, None, 
None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    7, None,    5, None, None, 
None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, None,    3, None, 
None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    3, None, None, 
None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, 
   5, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None,    5, 
None,   10, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, 
  10, None,    4, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, 
None,    4, None,    4, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, 
None, None,    4, None,    6, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, 
None, None, None,    6, None,    9, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, 
None, None, None, None,    9, None,    4, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, 
None, None, None, None, None,    4, None,    6, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, 
None, None, None, None, None, None,    6, None,    7, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, 
None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, 
None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
   3, None, None, None, None, None, None, None, None,    4, None,    3, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None,    8, None, None, None, None, None, None, None, None,    3, None,    8, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None,    6, None, None, None, None, None, None, None, None,    8, None,    7, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None,    4, None, None, None, None, None, None, None, None,    7, None,    6, None, None, None, None, None, None, None, None,    8, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None,    4, None, None, None, None, None, None, None, None,    6, None,    3, None, None, None, None, None, None, None, None,    4, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    3, None,   10, None, None, None, None, None, None, None, None,    5, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None,    3, None, None, None, None, None, None, None, None,   10, None,    4, None, None, None, None, None, None, None, None,    4, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    4, None,   10, None, None, None, None, None, None, None, None,    5, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None,    7 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    5, None,    6, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None, None, None, None, None,    6, None,    5, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None,    5, None,    3, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None,    3, None,   10, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,   10, None,    4, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    4, None,    7, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None,    7, None,    6, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None, None, None, None, None,    6, None,    6 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None,    6, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \
        [(0, 32, 13, 5), (1, 54, 80, 6), (2, 13, 10, 12), (3, 87, 56, 14), (4, 47, 19, 15), (5, 97, 77, 16), (6, 61, 63, 20), (7, 32, 31, 22), 
(8, 43, 30, 29), (9, 8, 29, 32), (10, 59, 76, 33), (11, 82, 53, 35), (12, 57, 85, 40), (13, 0, 34, 41), (14, 55, 97, 42), (15, 42, 41, 45), (16, 85, 66, 51), (17, 67, 55, 58), (18, 52, 93, 59), (19, 89, 99, 60), (20, 79, 55, 63), (21, 55, 85, 70), (22, 55, 78, 72), (23, 57, 95, 75), (24, 36, 17, 76), (25, 81, 64, 79), (26, 78, 97, 84), (27, 58, 96, 94), (28, 72, 93, 96), (29, 12, 42, 97), (30, 16, 9, 99), (31, 93, 70, 101), (32, 79, 58, 103), (33, 18, 16, 105), (34, 20, 0, 110), (35, 45, 9, 114), (36, 69, 99, 115), (37, 44, 41, 116), (38, 18, 26, 119), (39, 3, 24, 121), (40, 49, 9, 122), (41, 69, 97, 127), (42, 16, 15, 129), (43, 48, 27, 134), (44, 35, 37, 136), (45, 37, 15, 137), (46, 7, 45, 138), (47, 64, 82, 140), (48, 0, 31, 142), (49, 52, 61, 143), (50, 9, 38, 144), (51, 90, 94, 145), (52, 84, 80, 146), (53, 99, 67, 148), (54, 51, 71, 151), 
(55, 63, 94, 153), (56, 91, 70, 155), (57, 60, 53, 161), (58, 40, 31, 163), (59, 31, 22, 164), (60, 2, 24, 165), (61, 60, 84, 166), (62, 93, 90, 170), (63, 43, 21, 171), (64, 63, 61, 173), (65, 19, 16, 176), (66, 47, 26, 178), (67, 18, 5, 179), (68, 22, 23, 181), (69, 85, 89, 184), (70, 25, 16, 187), (71, 85, 57, 188), (72, 4, 34, 191), (73, 25, 29, 192), (74, 95, 69, 194), (75, 97, 77, 195), (76, 60, 51, 197), (77, 78, 97, 199), (78, 40, 3, 202), (79, 42, 44, 205), (80, 10, 30, 206), (81, 93, 70, 216), (82, 9, 39, 219), (83, 3, 0, 223), (84, 24, 11, 228), (85, 54, 
82, 229), (86, 94, 54, 230), (87, 96, 66, 231), (88, 25, 28, 233), (89, 70, 91, 234), (90, 2, 12, 235), (91, 95, 67, 236), (92, 28, 48, 240), (93, 28, 35, 241), (94, 61, 71, 243), (95, 53, 80, 244), (96, 41, 33, 246), (97, 33, 40, 247), (98, 36, 9, 251), (99, 46, 39, 255), (100, 18, 48, 256), (101, 8, 16, 258), (102, 49, 37, 259), (103, 83, 53, 265), (104, 98, 55, 267), (105, 53, 80, 271), (106, 7, 19, 272), (107, 51, 73, 277), (108, 19, 36, 279), (109, 98, 66, 287), (110, 92, 90, 290), (111, 18, 39, 293), (112, 30, 32, 294), (113, 4, 24, 297), (114, 11, 40, 298), (115, 71, 93, 299), (116, 54, 82, 300), (117, 9, 45, 303), (118, 63, 70, 304), (119, 37, 29, 306), (120, 29, 45, 307), (121, 68, 59, 310), (122, 23, 21, 313), (123, 37, 35, 315), (124, 95, 56, 316), (125, 97, 57, 322), (126, 27, 45, 329), (127, 44, 22, 330), (128, 28, 7, 334), (129, 41, 30, 336), (130, 44, 33, 338), (131, 12, 41, 339), (132, 75, 58, 340), (133, 35, 39, 342), (134, 73, 60, 346), (135, 80, 84, 353), (136, 99, 77, 354), (137, 81, 50, 355), (138, 45, 36, 356)]
        driverInfo = \
        [(0, 46), (1, 97), (2, 26), (3, 7), (4, 32), (5, 62), (6, 88), (7, 72), (8, 33), (9, 94), (10, 28), (11, 47), (12, 49), (13, 95), (14, 
82)]
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, start, dropoff, timestep in orderInfo:
            orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers

# TEST 7
# LAYOUT: 5x5 GRID
# 10 DRIVERS, 6 HOUR PERIOD   
# FLAT RATE $7/order
# EDGE DURATIONS RANGE (3, 10)
def test7():
        n = 5
        m = 5
        flatRate = 7
        totalMins = 360
        adjMatrix = \
        [
 [ None,    4, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    4, None,    8, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    8, None,    8, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    8, None,   10, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,   10, None, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    6, None, None, None, None, None,   10, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    5, None, None, None,   10, None,    5, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    6, None, None, None,    5, None,    5, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    8, None, None, None,    5, None,   10, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    6, None, None, None,   10, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    3, None, None, None, None, None,    6, None, None, None,    8, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    6, None, None, None,    6, None,    5, None, None, None,    3, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    3, None, None, None,    5, None,    7, None, None, None,    9, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    9, None, None, None,    7, None,    8, None, None, None,    6, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    9, None, None, None,    8, None, None, None, None, None,    3, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None,    3, None, None, None,    4, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None,    3, None,    4, None, None, None,    8, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None,    4, None,   10, None, None, None,    6, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None,   10, None,    8, None, None, None,   3, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None,    8, None, None, None, None, None,    8 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None,    9, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None,    9, None,    4, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None,    4, None,    3, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None,    3, None,    8 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None,    8, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \
        [(0, 6, 6, 0), (1, 18, 22, 2), (2, 3, 2, 4), (3, 6, 5, 6), (4, 2, 4, 8), (5, 21, 20, 10), (6, 18, 17, 14), (7, 16, 10, 18), (8, 10, 16, 19), (9, 4, 2, 22), (10, 11, 21, 26), (11, 5, 1, 27), (12, 21, 11, 28), (13, 13, 13, 29), (14, 7, 2, 31), (15, 0, 0, 35), (16, 21, 11, 38), (17, 16, 21, 43), (18, 13, 12, 46), (19, 24, 23, 47), (20, 22, 18, 50), (21, 22, 18, 66), (22, 11, 10, 67), (23, 17, 12, 68), (24, 20, 10, 69), (25, 22, 12, 73), (26, 1, 5, 74), (27, 11, 10, 76), (28, 14, 23, 79), (29, 13, 13, 81), (30, 22, 22, 84), (31, 13, 14, 90), (32, 5, 5, 92), (33, 5, 6, 95), (34, 12, 18, 100), (35, 16, 11, 101), (36, 16, 15, 102), (37, 15, 15, 103), (38, 16, 15, 104), (39, 23, 24, 105), (40, 16, 16, 106), (41, 14, 14, 107), (42, 15, 15, 122), (43, 7, 4, 123), (44, 18, 24, 124), (45, 3, 7, 131), (46, 21, 15, 132), (47, 0, 5, 135), (48, 22, 18, 136), (49, 24, 14, 138), (50, 16, 11, 140), (51, 10, 11, 141), (52, 22, 13, 142), (53, 9, 8, 146), (54, 16, 11, 148), (55, 1, 5, 149), (56, 18, 
13, 151), (57, 8, 4, 152), (58, 18, 22, 155), (59, 3, 7, 156), (60, 13, 14, 157), (61, 14, 24, 163), (62, 15, 21, 164), (63, 13, 23, 165), (64, 17, 18, 167), (65, 16, 15, 168), (66, 6, 5, 170), (67, 2, 3, 171), (68, 10, 10, 174), (69, 6, 5, 175), (70, 5, 5, 177), (71, 5, 6, 183), (72, 
8, 7, 187), (73, 5, 6, 190), (74, 4, 2, 192), (75, 0, 0, 193), (76, 18, 19, 194), (77, 9, 3, 202), (78, 19, 17, 206), (79, 16, 11, 211), (80, 22, 13, 213), (81, 3, 3, 221), (82, 17, 24, 223), (83, 18, 14, 233), (84, 17, 22, 241), (85, 17, 17, 243), (86, 15, 16, 244), (87, 19, 18, 246), (88, 12, 18, 249), (89, 12, 23, 250), (90, 18, 24, 252), (91, 21, 11, 253), (92, 17, 14, 256), (93, 20, 20, 262), (94, 2, 2, 264), (95, 6, 6, 
265), (96, 11, 21, 266), (97, 11, 15, 267), (98, 13, 13, 268), (99, 24, 12, 269), (100, 7, 4, 272), (101, 2, 9, 274), (102, 18, 13, 275), (103, 0, 5, 280), (104, 1, 1, 284), (105, 18, 18, 289), (106, 8, 7, 294), (107, 16, 11, 303), (108, 23, 17, 306), (109, 10, 16, 309), (110, 7, 8, 310), (111, 15, 11, 311), (112, 2, 7, 315), (113, 17, 12, 316), (114, 18, 18, 322), (115, 6, 5, 324), (116, 24, 12, 325), (117, 13, 12, 329), (118, 23, 24, 331), (119, 21, 10, 333), (120, 6, 0, 335), (121, 18, 23, 338), (122, 4, 8, 340), (123, 20, 15, 341), (124, 12, 23, 342), (125, 8, 8, 343), (126, 13, 23, 344), (127, 2, 8, 346), (128, 20, 21, 348), (129, 23, 18, 349), (130, 17, 14, 351), (131, 15, 20, 356), (132, 12, 14, 357)]
        driverInfo = \
        [(0, 2), (1, 13), (2, 6), (3, 17), (4, 15), (5, 24), (6, 19), (7, 11), (8, 16), (9, 8)]
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, start, dropoff, timestep in orderInfo:
            orderQueue.append(Order(id, start, dropoff, orderDuration, timestep, flatRate))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers

#########################################################################
################## TESTS WITH ORDER PROXIMITY & BASE PAY ################
#########################################################################

# TEST 8
# LAYOUT: 6x6 GRID
# 10 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $3/order
# EDGE DURATIONS RANGE (3, 10)
def test8():
        n = 6
        m = 6
        basePay = 3 # total price will be calculated later when assigned to driver
        totalMins = 360
        adjMatrix = \
        [
 [ None,    6, None, None, None, None,    5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    6, None,    4, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    4, None,    4, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    4, None,    4, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,    4, None,    3, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,    3, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [    5, None, None, None, None, None, None,    7, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None,    7, None, None, None, None,    7, None,    5, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None,    4, None, None, None, None,    5, None,    8, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None,   10, None, None, None, None,    8, None,    4, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None,   10, None, None, None, None,    4, None,    5, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None,    4, None, None, None, None,    5, None, None, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None,    4, None, None, None, None, None, None,    3, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None,    7, None, None, None, None,    3, None,    7, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    7, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    9, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    9, None,    6, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None,    6, None, None, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,   10, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,   10, None,   10, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None,   10, None,   10, None, None, None, None,    3, None, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None,   10, None,    6, None, None, None, None,    8, None, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    6, None,   10, None, None, None, None,    6, None, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None,   10, None, None, None, None, None, None,    8, None, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None, None, None,   10, None, None, None, None,    3, None, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,   10, None,    9, None, None, None, None,    7, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None,    9, None,    4, None, None, None, None,   10, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    4, None,    3, None, None, None, None,    4, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    3, None,    3, None, None, None, None,    8, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    3, None, None, None, None, None, None,    6 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None, None, None,   10, None, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None,   10, None,    4, None, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    4, None,    3, None, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None,    3, None,    7, None ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    4 ],
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    4, None ]
]
        map = GridLayout(n, m, n * m, adjMatrix)
        orderInfo = \
        [(0, 33, 31, 2), (1, 16, 9, 6), (2, 34, 27, 7), (3, 31, 32, 17), (4, 21, 22, 19), (5, 5, 3, 20), (6, 4, 3, 21), (7, 22, 29, 27), (8, 35, 29, 32), (9, 22, 27, 35), (10, 29, 23, 40), (11, 25, 24, 41), (12, 11, 17, 45), (13, 33, 21, 46), (14, 14, 27, 49), (15, 32, 33, 50), (16, 14, 27, 51), (17, 3, 11, 52), (18, 22, 23, 56), (19, 3, 2, 59), (20, 23, 28, 60), (21, 20, 26, 63), (22, 18, 12, 68), (23, 0, 18, 69), (24, 32, 28, 70), (25, 35, 34, 75), (26, 21, 15, 77), (27, 29, 34, 81), (28, 7, 8, 82), (29, 10, 4, 83), (30, 25, 19, 84), (31, 12, 6, 91), (32, 33, 27, 92), (33, 2, 14, 95), (34, 17, 11, 100), (35, 6, 12, 106), (36, 4, 17, 107), (37, 19, 13, 109), (38, 3, 5, 114), (39, 31, 30, 117), (40, 7, 8, 123), (41, 32, 33, 124), (42, 17, 10, 126), (43, 23, 28, 128), (44, 20, 8, 132), (45, 21, 20, 134), (46, 
4, 3, 136), (47, 18, 30, 139), (48, 9, 3, 140), (49, 33, 28, 141), (50, 3, 8, 146), (51, 7, 8, 147), (52, 24, 18, 148), (53, 8, 3, 151), (54, 14, 20, 152), (55, 6, 
12, 153), (56, 24, 30, 154), (57, 31, 32, 156), (58, 3, 9, 158), (59, 17, 11, 161), (60, 15, 10, 163), (61, 17, 11, 171), (62, 32, 28, 172), (63, 23, 11, 173), (64, 1, 8, 175), (65, 33, 32, 176), (66, 21, 27, 177), (67, 20, 26, 181), (68, 26, 27, 186), (69, 5, 2, 191), (70, 7, 6, 192), (71, 1, 2, 194), (72, 7, 6, 196), (73, 8, 14, 197), (74, 33, 20, 198), (75, 21, 20, 202), (76, 26, 27, 205), (77, 0, 18, 206), (78, 18, 12, 209), (79, 35, 29, 211), (80, 31, 25, 212), (81, 10, 9, 216), (82, 29, 35, 217), (83, 34, 29, 221), (84, 32, 31, 226), (85, 33, 27, 228), (86, 5, 3, 229), (87, 3, 2, 231), (88, 17, 11, 232), (89, 19, 20, 241), (90, 30, 24, 244), 
(91, 32, 31, 248), (92, 3, 5, 252), (93, 29, 27, 256), (94, 12, 6, 258), (95, 34, 27, 260), (96, 19, 18, 262), (97, 29, 27, 263), (98, 12, 7, 264), (99, 20, 27, 267), (100, 6, 0, 268), (101, 35, 29, 269), (102, 31, 32, 271), (103, 2, 3, 272), (104, 2, 3, 274), (105, 10, 17, 275), (106, 35, 33, 277), (107, 11, 4, 278), (108, 29, 28, 281), (109, 2, 9, 283), (110, 30, 18, 286), (111, 14, 12, 288), (112, 30, 24, 292), (113, 31, 32, 295), (114, 31, 30, 299), (115, 12, 6, 301), (116, 13, 12, 303), (117, 14, 27, 304), (118, 12, 14, 306), (119, 7, 2, 310), (120, 27, 32, 311), (121, 31, 32, 313), (122, 33, 27, 314), (123, 32, 31, 315), (124, 27, 26, 321), (125, 9, 21, 322), (126, 24, 30, 329), (127, 14, 27, 330), (128, 35, 29, 332), (129, 32, 27, 333), (130, 6, 13, 337), (131, 11, 10, 338), (132, 22, 23, 342), (133, 14, 26, 343), (134, 31, 30, 344), (135, 18, 24, 351), (136, 27, 26, 356), (137, 3, 2, 358)]
        driverInfo = \
        [(0, 34), (1, 14), (2, 19), (3, 4), (4, 1), (5, 3), (6, 25), (7, 5), (8, 5), (9, 5)]
        orderQueue = []
        drivers = []
        orderDuration = 0 # will update when assigned to driver
        # INIT ORDERS
        for id, pickup, dropoff, timestep in orderInfo:
            orderQueue.append(Order(id, pickup, dropoff, orderDuration, timestep, basePay))
        # INIT DRIVERS
        for id, start in driverInfo:
            drivers.append(Driver(id, start))

        return map, orderQueue, totalMins, drivers
