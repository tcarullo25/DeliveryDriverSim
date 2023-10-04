from graphs import *
from ordersAndDrivers import *

# TEST 1
# LAYOUT: 5x5 GRID
# 8 DRIVERS, 6 HOUR PERIOD
# FLAT RATE $7/order
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

    map = GridLayout(n, m, n*m)
    map.adjMatrix = adjMatrix
    
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
        