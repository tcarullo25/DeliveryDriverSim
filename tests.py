from graphs import *
from ordersAndDrivers import *
import random

# https://www.kosbie.net/cmu/spring-21/15-112/notes/notes-2d-lists.html
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')

def genTest(n, m, flatRate, numDrivers, durationRange, orderSpawnRate, totalMins):
    randomMap = RandomGridLayout(n, m, n * m, durationRange)
    orderCount = 0
    orderDuration = 0 
    numNodes = n * m 
    orderQueue = []
    drivers = [(i, random.randint(0, numNodes-1)) for i in range(0, numDrivers)]
    for minute in range(totalMins):
        if random.random() < orderSpawnRate:
            start = random.randint(0, numNodes-1)
            dest = random.randint(0, numNodes - 1)
            orderQueue.append((orderCount, start, dest, orderDuration, minute, flatRate))
            orderCount += 1
    #print("ADJACENCY MATRIX:\n", randomMap.adjMatrix)
    #print("DRIVERS:\n", drivers)
    #print("ORDER QUEUE:\n", orderQueue)

genTest(6, 6, 7, 9, (3, 10), .4, 360)


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
    # RANDOM GEN DURATIONS (RANGE 5, 30)
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
    for id, start, dest, timestep in orderInfo:
        orderQueue.append(Order(id, start, dest, orderDuration, timestep, flatRate))
    # INIT DRIVERS
    for id, start in driverInfo:
        drivers.append(Driver(id, start))

    return  map, orderQueue, totalMins, drivers


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
 [ None,    7, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [    7, None,    9, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None,    9, None,    4, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None,    4, None,   10, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None,   10, None,    8, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None,    8, None, None, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [    7, None, None, None, None, None, None,    3, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None,    8, None, None, None, None,    3, None,    7, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None,    4, None, None, None, None,    7, None,    6, None, None, None, None,    8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None,    4, None, None, None, None,    6, None,    9, None, None, None, None,    3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None,   10, None, None, None, None,    9, None,   10, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None,    8, None, None, None, None,   10, None, None, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None,    9, None, None, None, None, None, None,    9, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None,    9, None, None, None, None,    9, None,    7, None, None, None, None,   10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    4, None, None, None, None,    4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None,    3, None, None, None, None,    4, None,    7, None, None, None, None,    6, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    7, None,    3, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None, None, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None,    3, None, None, None, None,    9, None, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None,    7, None, None, None, None,    7, None, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None,    4, None, None, None, None,    7, None,    9, None, None, None, None,    5, None, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    9, None,    3, None, None, None, None,    8, None, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None,    3, None,    5, None, None, None, None,    8, None, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None,    5, None, None, None, None, None, None,   10, None, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    9, None, None, None, None, None, None,    5, None, None, None, None,    8, None, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    7, None, None, None, None,    5, None,    4, None, None, None, None,   10, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    5, None, None, None, None,    4, None,    3, None, None, None, None,    8, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    3, None,    5, None, None, None, None,    8, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    5, None,    3, None, None, None, None,    6, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None, None, None, None, None, None,    3 ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None, None, None,    3, None, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,   10, None, None, None, None,    3, None,    7, None, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    7, None,    4, None, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    8, None, None, None, None,    4, None,    3, None ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    6, None, None, None, None,    3, None,    3 ]
 [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    3, None, None, None, None,    3, None ]
]



'''DRIVERS:
 [(0, 8), (1, 11), (2, 16), (3, 33), (4, 33), (5, 9), (6, 20), (7, 12), (8, 23)]
ORDER QUEUE:
 [(0, 33, 17, 0, 0, 7), (1, 6, 25, 0, 2, 7), (2, 23, 14, 0, 4, 7), (3, 11, 4, 0, 5, 7), (4, 10, 30, 0, 6, 7), (5, 28, 34, 0, 7, 7), (6, 11, 4, 0, 10, 7), (7, 33, 24, 0, 11, 7), (8, 22, 13, 0, 13, 7), (9, 32, 22, 0, 17, 7), (10, 14, 25, 0, 22, 7), (11, 18, 0, 0, 27, 7), (12, 17, 6, 0, 29, 7), (13, 35, 8, 0, 30, 7), (14, 2, 17, 0, 33, 7), (15, 26, 31, 0, 39, 7), (16, 28, 8, 0, 41, 7), (17, 18, 12, 0, 43, 7), (18, 7, 19, 0, 45, 7), (19, 2, 1, 0, 51, 7), (20, 6, 1, 0, 54, 7), (21, 11, 28, 0, 55, 7), (22, 0, 26, 0, 56, 7), (23, 12, 33, 0, 60, 7), (24, 15, 4, 0, 66, 7), (25, 23, 34, 0, 71, 7), (26, 6, 15, 0, 73, 7), (27, 10, 23, 0, 77, 7), (28, 13, 3, 0, 78, 7), (29, 33, 7, 0, 79, 7), (30, 15, 18, 0, 81, 7), (31, 25, 4, 0, 82, 7), (32, 29, 1, 0, 84, 7), (33, 34, 32, 0, 85, 7), (34, 6, 29, 0, 89, 7), (35, 10, 16, 0, 91, 7), (36, 22, 7, 0, 93, 7), (37, 10, 25, 0, 96, 7), (38, 13, 1, 0, 97, 7), (39, 20, 16, 0, 98, 7), (40, 31, 5, 0, 99, 7), (41, 7, 7, 0, 102, 7), (42, 2, 24, 0, 104, 7), (43, 12, 13, 0, 105, 7), (44, 3, 4, 0, 109, 7), (45, 10, 8, 0, 110, 7), (46, 16, 25, 0, 115, 7), (47, 18, 1, 0, 116, 7), (48, 6, 6, 0, 124, 7), (49, 27, 23, 0, 125, 7), (50, 8, 30, 0, 128, 7), (51, 35, 25, 0, 129, 7), (52, 28, 18, 0, 132, 7), (53, 25, 32, 0, 134, 7), (54, 15, 21, 0, 139, 7), (55, 18, 18, 0, 140, 7), (56, 7, 4, 0, 144, 7), (57, 10, 1, 0, 145, 7), (58, 6, 27, 0, 146, 7), (59, 7, 12, 0, 148, 7), (60, 14, 10, 0, 
151, 7), (61, 8, 9, 0, 158, 7), (62, 11, 3, 0, 159, 7), (63, 11, 33, 0, 166, 7), (64, 32, 7, 0, 169, 7), (65, 30, 2, 0, 172, 7), (66, 23, 25, 0, 173, 7), (67, 7, 32, 0, 174, 7), (68, 11, 18, 0, 175, 7), (69, 7, 9, 0, 176, 7), (70, 5, 8, 
0, 181, 7), (71, 25, 24, 0, 182, 7), (72, 20, 31, 0, 186, 7), (73, 3, 22, 0, 187, 7), (74, 26, 25, 0, 189, 7), (75, 33, 35, 0, 190, 7), (76, 17, 6, 0, 191, 7), (77, 5, 27, 0, 196, 7), (78, 16, 32, 0, 197, 7), (79, 30, 5, 0, 199, 7), (80, 26, 19, 0, 200, 7), (81, 0, 25, 0, 201, 7), (82, 29, 10, 0, 204, 7), (83, 28, 0, 0, 206, 7), (84, 10, 10, 0, 208, 7), (85, 29, 23, 0, 209, 7), (86, 28, 6, 0, 217, 7), (87, 7, 18, 0, 220, 7), (88, 4, 33, 0, 226, 7), (89, 4, 33, 0, 227, 7), (90, 13, 1, 0, 235, 7), (91, 7, 1, 0, 236, 7), (92, 30, 16, 0, 239, 7), (93, 29, 29, 0, 243, 7), (94, 33, 28, 0, 245, 7), (95, 4, 14, 0, 246, 7), (96, 17, 24, 0, 247, 7), (97, 0, 30, 0, 252, 7), (98, 11, 1, 0, 253, 7), (99, 22, 27, 0, 254, 7), (100, 21, 22, 0, 256, 7), (101, 19, 28, 0, 258, 7), (102, 29, 7, 0, 259, 7), (103, 20, 5, 0, 260, 7), (104, 16, 17, 0, 262, 7), (105, 3, 13, 0, 266, 7), (106, 3, 31, 0, 267, 7), (107, 8, 2, 0, 268, 7), (108, 16, 24, 0, 272, 7), (109, 21, 12, 0, 279, 7), (110, 32, 35, 0, 282, 7), (111, 30, 16, 0, 287, 7), (112, 14, 28, 0, 290, 7), (113, 19, 32, 0, 292, 7), (114, 19, 21, 0, 299, 7), (115, 16, 15, 0, 301, 7), (116, 29, 26, 0, 302, 7), (117, 7, 6, 0, 307, 7), (118, 0, 15, 0, 310, 7), (119, 4, 24, 0, 311, 7), (120, 22, 16, 0, 312, 7), (121, 14, 30, 0, 320, 7), (122, 27, 26, 0, 321, 7), (123, 29, 0, 0, 323, 7), (124, 27, 18, 0, 327, 7), (125, 0, 34, 0, 330, 7), (126, 9, 14, 0, 331, 7), (127, 24, 34, 0, 336, 7), (128, 33, 27, 0, 339, 7), (129, 12, 4, 0, 341, 7), (130, 17, 14, 0, 342, 7), (131, 14, 25, 0, 344, 7), (132, 23, 5, 0, 346, 7), (133, 8, 1, 0, 349, 7), (134, 4, 3, 0, 351, 7), (135, 5, 10, 0, 352, 7), (136, 13, 13, 0, 354, 
7), (137, 23, 28, 0, 356, 7)]'''