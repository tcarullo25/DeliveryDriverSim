from graphs import *
from ordersAndDrivers import * 
from tests import *
from visualizations import *

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

def getFurthestDriverDuration(map, drivers, currOrder):
    furthestDur = None
    for driver in drivers:
        currLocToOrderDuration, _ = getOrderDuration(map, driver.currLoc, currOrder.pickup, currOrder.dropoff)
        if furthestDur == None or currLocToOrderDuration > furthestDur:
            furthestDur = currLocToOrderDuration
    return furthestDur

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

def initSim(map, orderQueue, drivers, totalMins):
    # keep track of order info for data visualizations
    ordersCompleted = 0
    delayedOrders = 0
    finishedOrders = []
    # flat rate added to base pay for every order
    hourlyRate = 25

    for minute in range(totalMins):
        # ORDER ASSIGNMENT LOGIC #
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].releaseTime <= minute:
            currOrder = orderQueue[0]
            availableDrivers = getAvailableDrivers(drivers)
            # can only assign order if there is an open driver
            if availableDrivers:
                currOrder = orderQueue.pop(0)
                bestDriver, (currLocToOrderPickup, totalDuration) = getBestDriver(map, availableDrivers, currOrder)
                # the order's price will be the lower of base pay or rate calculated from pickup to dropoff duration
                rate = min(currOrder.price, hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
                currOrder.price = rate
                driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
                currOrder.driverToPickupDur = currLocToOrderPickup * driverReliabilityFactor
                pickupToDeliverDur = totalDuration - currLocToOrderPickup
                currOrder.pickupToDeliverDur = pickupToDeliverDur * driverReliabilityFactor
                bestDriver.addOrder(currOrder)
            else:
                # if not already delayed
                if orderQueue[0].delayedInAssignmentDuration == 0:
                    delayedOrders += 1
                orderQueue[0].delayedInAssignmentDuration += 1
        # DRIVER LOGIC #
        for driver in drivers:
                if driver.order != None:
                    driver.checkOrder(minute)
                    # check if completed order and if so reflect driver's status
                    if driver.order.delivered:
                        ordersCompleted += 1
                        finishedOrders.append(driver.order)
                        driver.updateReputation()
                        driver.completeOrder()
                else:
                    driver.idleTime += 1
                    driver.nonproductiveTime += 1
                driver.reputationOverTime.append(driver.reputation)

    return drivers, (ordersCompleted, delayedOrders, finishedOrders)

def displayResults(drivers, orderInfo, totalMins):
    ordersCompleted, _, _ = orderInfo
    res = f'SEED: {seed}\nTEST: {testNum}\n'
    res += f'There was a total of {ordersCompleted} orders completed across all drivers.\nThe earnings for each driver are as follows:\n'
    sumOfRates = 0
    for driver in drivers:
        driver.earnings = round(driver.earnings, 2)
        driverRate = driver.earnings / (totalMins/60)
        sumOfRates += driverRate
        res += f'• Driver {driver.id} received ${driver.earnings}, completed {driver.totalOrders} orders and it took them {driver.totalOrderTime} timesteps with a reputation of {driver.reputation}.\n'
    avgRate = round(sumOfRates/len(drivers),2)
    res += f'The average wage across all drivers is: ${avgRate}/hr'
    print(res)
    displayVisualizations(drivers, orderInfo, avgRate, totalMins)

def chooseLayout(graphType, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins, drivers = eval(f'test{testNum}()')

    drivers, orderInfo = initSim(map, orderQueue,  drivers, totalMins)
    displayResults(drivers, orderInfo, totalMins)

graphType = 'grid'
testNum = 8
seed = 1

#NOTE: seed dictates randomness of drivers' lateness
random.seed(seed)

chooseLayout(graphType, testNum)
