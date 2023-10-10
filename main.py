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

def getClosestDriver(map, drivers, currOrder):
    bestDur = None
    bestDriver = None
    for driver in drivers:
        currLocToOrderDuration, totalTime = getOrderDuration(map, driver.currLoc, currOrder.pickup, currOrder.dropoff)
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
    # keep track of order info for data visualizations
    ordersCompleted = 0
    delayedOrders = 0
    finishedOrders = []
    # flat rate added to base pay for every order
    hourlyRate = 14

    for minute in range(totalMins):
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].timestep <= minute:
            currOrder = orderQueue[0]
            availableDrivers = getAvailableDrivers(drivers)
            # can only assign order if there is an open driver
            if availableDrivers:
                currOrder = orderQueue.pop(0)
                closestDriver, (currLocToOrderPickup, totalDuration) = getClosestDriver(map, availableDrivers, currOrder)
                #orderPickupToDropoffDuration = totalDuration - currLocToOrderPickup
                #NOTE: using total order duration b/c orderPickUpToDropoff is too small
                rate = (totalDuration/60) * hourlyRate
                currOrder.price += rate
                currOrder.duration = totalDuration
                currOrder.driverToPickupDur = currLocToOrderPickup
                closestDriver.addOrder(currOrder)
            else:
                # if not already delayed
                if orderQueue[0].delayedLength == 0:
                    delayedOrders += 1
                orderQueue[0].delayedLength += 1

        for driver in drivers:
                if driver.order != None:
                    # decrease order duration by one timestep
                    # increase driver's curr order time
                    driver.order.duration -= 1
                    driver.currOrderTime += 1
                    # have not arrived at restaurant yet
                    if driver.currOrderTime < driver.order.driverToPickupDur:
                        driver.nonproductiveTime += 1
                    # check if completed order and if so reflect driver's status
                    if driver.order.duration <= 0:
                        ordersCompleted += 1
                        finishedOrders.append(driver.order)
                        driver.currLoc = driver.order.dropoff
                        driver.earnings += driver.order.price
                        driver.totalOrders += 1
                        driver.totalOrderTime += driver.currOrderTime
                        driver.orderTimes.append(driver.currOrderTime)
                        driver.currOrderTime = 0
                        driver.order = None
                else:
                    driver.idleTime += 1
                    driver.nonproductiveTime += 1

    return drivers, (ordersCompleted, delayedOrders, finishedOrders)

def displayResults(drivers, orderInfo, totalMins):
    ordersCompleted, _, _ = orderInfo
    res = f'There was a total of {ordersCompleted} orders completed across all drivers.\nThe earnings for each driver are as follows:\n'
    sumOfRates = 0
    for driver in drivers:
        driver.earnings = round(driver.earnings, 2)
        driverRate = driver.earnings / (totalMins/60)
        sumOfRates += driverRate
        res += f'• Driver {driver.id} received ${driver.earnings}, completed {driver.totalOrders} orders and it took them {driver.totalOrderTime} timesteps.\n'
    avgRate = round(sumOfRates/len(drivers),2)
    res += f'The average wage across all drivers is: ${avgRate}/hr'
    print(res)
    displayVisualizations(drivers, orderInfo, avgRate)

def chooseLayout(graphType, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins, drivers = eval(f'test{testNum}()')

    drivers, orderInfo = initSim(map, orderQueue,  drivers, totalMins)
    displayResults(drivers, orderInfo, totalMins)

graphType = 'grid'
testNum = 8
chooseLayout(graphType, testNum)
