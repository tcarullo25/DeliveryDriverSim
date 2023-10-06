from graphs import *
from ordersAndDrivers import * 
from tests import *
from visualizations import *

def getOrderDuration(map, currLoc, orderLoc, orderDest):
    currToOrderSP = nx.shortest_path(map.G, 
                    source=currLoc, target=orderLoc, weight = 'weight')
    orderToDestSP = nx.shortest_path(map.G, 
                    source=orderLoc, target=orderDest, weight = 'weight')
    totalTime = 0
    currLocToOrderDuration = 0

    # currLoc -> orderLoc duration
    for i in range(1, len(currToOrderSP)):
        currNode, prevNode = currToOrderSP[i], currToOrderSP[i-1]
        duration = map.adjMatrix[currNode][prevNode]
        totalTime += duration

    currLocToOrderDuration = totalTime

    # orderLoc -> orderDest duration
    for i in range(1, len(orderToDestSP)):
        currNode, prevNode = orderToDestSP[i], orderToDestSP[i-1]
        duration = map.adjMatrix[currNode][prevNode]
        totalTime += duration

    return currLocToOrderDuration, totalTime

def getClosestDriver(map, drivers, currOrder):
    bestDur = None
    bestDriver = None
    for driver in drivers:
        currLocToOrderDuration, totalTime = getOrderDuration(map, driver.currLoc, currOrder.loc, currOrder.dest)
        # only compare duration from curr loc to order location, not total time
        if bestDur == None or currLocToOrderDuration < bestDur[0]:
            bestDur = currLocToOrderDuration, totalTime
            bestDriver = driver
    return bestDriver, bestDur

def getAvailableDrivers(drivers):
    availableDrivers = []
    for driver in drivers:
        if driver.order == None:
            availableDrivers.append(driver)
    return availableDrivers

def initSim(map, orderQueue, drivers, totalMins):
    # KEEP TRACK OF ORDER INFORMATION FOR DATA VISUALIZATIONS
    ordersCompleted = 0
    delayedOrders = 0
    finishedOrders = []

    for minute in range(totalMins):
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].timestep <= minute:
            currOrder = orderQueue[0]
            availableDrivers = getAvailableDrivers(drivers)
            # can only assign order if there is an open driver
            if availableDrivers:
                currOrder = orderQueue.pop(0)
                closestDriver, (_, totalDuration) = getClosestDriver(map, availableDrivers, currOrder)
                currOrder.duration = totalDuration
                closestDriver.addOrder(currOrder)
            else:
                # if not already delayed
                if orderQueue[0].delayedLength == 0:
                    delayedOrders += 1
                orderQueue[0].delayedLength += 1

        for driver in drivers:
                if driver.order != None:
                    # decrease order duration by one timestep,
                    # increase driver's curr order time
                    driver.order.duration -= 1
                    driver.currOrderTime += 1
                    # check if completed order and if so reflect driver's status
                    if driver.order.duration <= 0:
                        ordersCompleted += 1
                        finishedOrders.append(driver.order)
                        driver.currLoc = driver.order.loc
                        driver.earnings += driver.order.price
                        driver.totalOrders += 1
                        driver.totalOrderTime += driver.currOrderTime
                        driver.orderTimes.append(driver.currOrderTime)
                        driver.currOrderTime = 0
                        driver.order = None
                else:
                    driver.idleTime += 1
    return drivers, (ordersCompleted, delayedOrders, finishedOrders)

def displayVisualizations(drivers, orderInfo, avgRate):
    ordersCompleted, delayedOrders, finishedOrders = orderInfo
    plotDriverEarnings(drivers, avgRate)
    plotOrderTimes(drivers)
    plotOrdersPerDriver(drivers)
    plotDeliveryDurations(drivers)
    plotIdleTimes(drivers)
    plotDelayedOrders(ordersCompleted, delayedOrders)
    allOrders = [driver.order for driver in drivers if driver.order] + finishedOrders
    plotOrderDelayDurations(allOrders)

def displayResults(drivers, orderInfo, totalMins):
    ordersCompleted, _, _ = orderInfo
    res = f'There was a total of {ordersCompleted} orders completed across all drivers.\nThe earnings for each driver are as follows:\n'
    sumOfRates = 0
    for driver in drivers:
        driverRate = driver.earnings / (totalMins/60)
        sumOfRates += driverRate
        res += f'• Driver {driver.id} received ${driver.earnings}, completed {driver.totalOrders} orders and it took them {driver.totalOrderTime} timesteps.\n'
    avgRate = sumOfRates/len(drivers)
    res += f'The average wage across all drivers is: ${round(avgRate, 2)}/hr'
    print(res)
    displayVisualizations(drivers, orderInfo, avgRate)

def chooseLayout(graphType, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins, drivers = eval(f'test{testNum}()')

    drivers, orderInfo = initSim(map, orderQueue,  drivers, totalMins)
    displayResults(drivers, orderInfo, totalMins)

graphType = 'grid'
testNum = 7
chooseLayout(graphType, testNum)
