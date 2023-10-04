from graphs import *
from ordersAndDrivers import * 
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

def initSim(map, numNodes, numDrivers, totalMins):
    drivers = []
    for i in range(numDrivers):
        # get random starting location and assign driver ID
        startLoc = random.randint(0, numNodes-1)
        drivers.append(Driver(i, startLoc))

    orderSpawnrate = .4 
    flatFee = 7
    ordersCompleted = 0
    orderQueue = []
    
    for minute in range(totalMins):
        # check if new order has spawned
        if random.random() < orderSpawnrate:
            #NOTE: could be the same location as a driver
            orderLoc = random.randint(0, numNodes-1)
            orderDest = random.randint(0, numNodes-1)
            orderDuration = 0 # will update when assigned to driver
            id = minute
            currOrder = Order(id, orderLoc, orderDest, orderDuration, flatFee)
            orderQueue.append(currOrder)

        if orderQueue:
            currOrder = orderQueue.pop(0)
            closestDriver, duration = getClosestDriver(map, drivers, currOrder)
            currOrder.duration = duration
            closestDriver.addOrder(currOrder)

        for driver in drivers:
                if driver.order != None:
                    # order duration decrease by one timestep
                    driver.order.duration -= 1
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
        res += f'• Driver {driver.id} received ${driver.earnings} and completed {driver.totalOrders} orders\n'
    avgRate = sumOfRates/len(drivers)
    res += f'The average wage across all drivers is: ${round(avgRate, 2)}/hr'
    #print(res)
    return avgRate

def chooseLayout(graphType, n, m, numNodes, numDrivers, totalMins):
    if graphType == 'grid':
        map = GridLayout(n, m, numNodes)
    drivers, ordersCompleted = initSim(map, numNodes, numDrivers, totalMins)
    print(map.adjMatrix)
    return displayResults(drivers, ordersCompleted, totalMins)

graphType = 'grid'
n = 5
m = 5
numNodes = n*m
numDrivers = 15
totalMins = 360
chooseLayout(graphType, n, m, numNodes, numDrivers, totalMins)


#UNCOMMENT FOR MORE IN-DEPTH ANALYSIS
#import statistics
#res = []
#for numDrivers in range(20, 220, 20):
#    data = []
#    for _ in range(100):
#        data.append(chooseLayout(graphType, n, m, numNodes, numDrivers, totalMins))
#    res.append(statistics.median(data))
#print(res)
