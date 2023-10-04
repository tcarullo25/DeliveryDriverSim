from graphs import *
from ordersAndDrivers import * 
from tests import *

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
    ordersCompleted = 0

    for minute in range(totalMins):
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].timestep <= minute:
            currOrder = orderQueue[0]
            availableDrivers = getAvailableDrivers(drivers)
            # can only assign order if there is an open driver
            if availableDrivers:
                currOrder = orderQueue.pop(0)
                closestDriver, (_, duration) = getClosestDriver(map, availableDrivers, currOrder)
                currOrder.duration = duration
                closestDriver.addOrder(currOrder)

        for driver in drivers:
                if driver.order != None:
                    # decrease order duration by one timestep,
                    # increase driver's total order time
                    driver.order.duration -= 1
                    driver.totalOrderTime += 1

                    # check if completed order and if so reflect driver's status
                    if driver.order.duration <= 0:
                        ordersCompleted += 1
                        driver.currLoc = driver.order.loc
                        driver.totalOrders += 1
                        driver.earnings += driver.order.price
                        driver.order = None

    return drivers, ordersCompleted

def displayResults(drivers, ordersCompleted, totalMins):
    res = f'There was a total of {ordersCompleted} orders completed across all drivers.\nThe earnings for each driver are as follows:\n'
    sumOfRates = 0
    for driver in drivers:
        driverRate = driver.earnings / (totalMins/60)
        sumOfRates += driverRate
        res += f'• Driver {driver.id} received ${driver.earnings}, completed {driver.totalOrders} orders and it took them {driver.totalOrderTime} timesteps.\n'
    avgRate = sumOfRates/len(drivers)
    res += f'The average wage across all drivers is: ${round(avgRate, 2)}/hr'
    print(res)
    return avgRate

def chooseLayout(graphType, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins, drivers = eval(f'test{testNum}()')

    drivers, ordersCompleted = initSim(map, orderQueue,  drivers, totalMins)
    return displayResults(drivers, ordersCompleted, totalMins)

graphType = 'grid'
testNum = 4
chooseLayout(graphType, testNum)

#UNCOMMENT FOR MORE IN-DEPTH ANALYSIS
#import statistics
#res = []
#for numDrivers in range(20, 220, 20):
#    data = []
#    for _ in range(100):
#        data.append(chooseLayout(graphType, n, m, numNodes, numDrivers, totalMins))
#    res.append(statistics.median(data))
#print(res)
