import networkx as nx

def getBestDriver(map, drivers, currOrder):
    bestScore = float('-inf')
    bestDriver = None
    bestDur = None
    maxDuration = getFurthestDriverDuration(map, drivers, currOrder)
    for driver in drivers:
        currLocToOrderDuration, totalTime = getOrderDuration(map, driver.currLoc, currOrder.pickup, currOrder.dropoff)
        score = driver.computeDriverOrderScore(currLocToOrderDuration, maxDuration)
        if score > bestScore:
            bestScore = score
            bestDriver = driver
            bestDur = currLocToOrderDuration, totalTime 
    return bestDriver, bestDur

def getAvailableDrivers(drivers):
    availableDrivers = []
    for driver in drivers:
        if driver.order == None:
            availableDrivers.append(driver)
    return availableDrivers

def getFurthestDriverDuration(map, drivers, currOrder):
    furthestDur = None
    for driver in drivers:
        currLocToOrderDuration, _ = getOrderDuration(map, driver.currLoc, currOrder.pickup, currOrder.dropoff)
        if furthestDur == None or currLocToOrderDuration > furthestDur:
            furthestDur = currLocToOrderDuration
    return furthestDur

def getOrderDuration(map, currLoc, orderPickup, orderDropOff):
    currToOrderSP = nx.shortest_path(map.G, 
                    source=currLoc, target=orderPickup, weight = 'weight')
    orderToDestSP = nx.shortest_path(map.G, 
                    source=orderPickup, target=orderDropOff, weight = 'weight')
    totalTime = 0
    currLocToOrderDuration = 0

    # currLoc -> orderPickup duration
    for i in range(1, len(currToOrderSP)):
        currNode, prevNode = currToOrderSP[i], currToOrderSP[i-1]
        duration = map.adjMatrix[currNode][prevNode]
        totalTime += duration

    currLocToOrderDuration = totalTime

    # orderPickup -> orderDropOff duration
    for i in range(1, len(orderToDestSP)):
        currNode, prevNode = orderToDestSP[i], orderToDestSP[i-1]
        duration = map.adjMatrix[currNode][prevNode]
        totalTime += duration

    return currLocToOrderDuration, totalTime

def driverDecide(drivers, durs, currOrder, minute):
    remainingDrivers = []
    for i in range(len(drivers)):
        driver = drivers[i]
        currLocToOrderDuration, totalTime = durs[i]
        # if driver policy accepts order add it to remaining drivers
        if driver.policy(driver, currOrder, minute, currLocToOrderDuration, totalTime):
            remainingDrivers.append(driver)
    return remainingDrivers