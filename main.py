from graphs import *
from ordersAndDrivers import * 
from tests import *
import random
 
def getOrderDuration(map, currLoc, orderLoc):
    shortestPath = nx.shortest_path(map.G, 
                    source=currLoc, target=orderLoc)
    totalTime = 0

    for i in range(1, len(shortestPath)):
        currNode, prevNode = shortestPath[i], shortestPath[i-1]
        duration = map.adjMatrix[currNode][prevNode]
        totalTime += duration

    return totalTime

def getClosestDriver(map, drivers, currOrder):
    bestDur = None
    bestDriver = None
    for driver in drivers:
        currDriverDuration = getOrderDuration(map, driver.currLoc, currOrder.loc)
        if bestDur == None or currDriverDuration < bestDur:
            bestDur = currDriverDuration
            bestDriver = driver
    return bestDriver, bestDur

def initSim(map, orderQueue, numNodes, numDrivers, totalMins):
    drivers = []

    for i in range(numDrivers):
        # get random starting location and assign driver ID
        startLoc = random.randint(0, numNodes-1)
        drivers.append(Driver(i, startLoc))

    ordersCompleted = 0

    for minute in range(totalMins):
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].timestep == minute:
            currOrder = orderQueue.pop(0)
            closestDriver, duration = getClosestDriver(map, drivers, currOrder)
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

def chooseLayout(graphType, numNodes, numDrivers, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins = eval(f'test{testNum}()')
    #print("matrix:\n", map.adjMatrix)
    #print()

    drivers, ordersCompleted = initSim(map, orderQueue, numNodes, numDrivers, totalMins)
    return displayResults(drivers, ordersCompleted, totalMins)

graphType = 'grid'
n = 5
m = 5
numNodes = n*m
numDrivers = 15
testNum = 1
chooseLayout(graphType, numNodes, numDrivers, testNum)

#UNCOMMENT FOR MORE IN-DEPTH ANALYSIS
#import statistics
#res = []
#for numDrivers in range(20, 220, 20):
#    data = []
#    for _ in range(100):
#        data.append(chooseLayout(graphType, n, m, numNodes, numDrivers, totalMins))
#    res.append(statistics.median(data))
#print(res)
