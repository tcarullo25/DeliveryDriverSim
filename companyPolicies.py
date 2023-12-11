from driverHelperFns import *

## COMPANY INTERFACE ##
class Company():
    def __init__(self, clusters, map, totalMins):
        self.delayedOrders = 0
        self.hourlyRate = 25
        self.orderLog = {} 
        self.driverLog = [None for _ in range(totalMins)]
        self.clusters = self.getCentersOfClusters(clusters, map)

    def getCentersOfClusters(self, clusters, map):
        centers = []
        for cluster in clusters:
            topLeft, width, height = cluster
            centerRow = topLeft[0] + height // 2
            centerCol = topLeft[1] + width // 2
            centerNode = centerRow * map.m + centerCol
            centers.append(centerNode)
        return centers
    
    def orderStep(self, map, orderQueue, drivers, basePay, totalMins):
        pass

    def incDelayedInAsssignmentOrders(self, orderQueue, minute):
        for order in orderQueue:
            if order.releaseTime < minute:
                if order.delayedInAssignmentDuration == 0:
                    self.delayedOrders += 1
                order.delayedInAssignmentDuration += 1

    def finishSim(self):
        return self.delayedOrders, self.orderLog, self.driverLog

class KBestDriversPolicy(Company):
    def __init__(self, clusters, map, totalMins):
        super().__init__(clusters, map, totalMins)
        self.delayedQueue = []

    def assignDriver(self, map, drivers, currOrder, minute, basePay):
        bestDrivers, bestDurs = getKBestDrivers(map, drivers, currOrder)
        # see who accepts 
        remainingDrivers = driverDecide(bestDrivers, bestDurs, currOrder, minute)
        if not remainingDrivers:
            # add bestDrivers and the currOrder to a delayedQueue
            # check delayedQueue before orderQueue - check if nonempty
            # if so increment order price and run driverDecide again
            currOrder.additionalCompensation += 1
            self.delayedQueue.append((currOrder, bestDrivers, bestDurs))
        else:
            acceptedDrivers = [acceptedDriver.id for acceptedDriver in remainingDrivers]
            self.orderLog[currOrder.id] = [(driver, driver.reputation, driver.currLoc, acceptedDrivers) for driver in drivers]
        # get the best driver out of the previous best drivers who accepted order
        #NOTE: the best driver will be in terms of JUST the remaining drivers (the max duration likely changed), 
        # so the answer may slightly vary from what the single-most best driver was before
            bestDriver, (currLocToOrderPickup, totalDuration) = getBestDriver(map, remainingDrivers, currOrder)
            # every order is at least the base rate
            rate = max(basePay, self.hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
            currOrder.price = rate
            driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
            # get scaled driver durs by tracing through route
            setOrderIntermediateDurations(map, driverReliabilityFactor, currOrder, bestDriver.currLoc, currOrder.pickup, currOrder.dropoff)
            currOrder.driverToPickupDur = currOrder.intermediateEdges.getScaledPickupTime()
            currOrder.pickupToDeliverDur = currOrder.intermediateEdges.getScaledDeliverTime()
            bestDriver.addOrder(currOrder)
            currOrder.addDriver(bestDriver)

    def checkDelayedOrders(self, map, minute, basePay):
        newDelayedQueue = []
        for (order, bestDrivers, bestDurs) in self.delayedQueue:
            # get the best drivers for the given order and check who is still available 
            delayedBestDrivers = getAvailableDrivers(bestDrivers) 
            delayedRemainingDrivers = driverDecide(delayedBestDrivers, bestDurs, order, minute)
            # if no driver still does not want to take it, add order back to queue
            if not delayedRemainingDrivers:
                # to compute new price, get the average duration for order to approximate rate
                avgCurrLocToOrderPickup, avgTotalDuration = getAvgDurs(bestDurs)
                rate = min(basePay, self.hourlyRate * ((avgTotalDuration - avgCurrLocToOrderPickup)/60))   
                order.additionalCompensation += 1             
                order.price = rate + order.additionalCompensation                
                newDelayedQueue.append((order, delayedBestDrivers, bestDurs))
            else:
                acceptedDrivers = [acceptedDriver.id for acceptedDriver in delayedRemainingDrivers]
                self.orderLog[order.id] = [(driver, driver.reputation, driver.currLoc, acceptedDrivers) for driver in delayedBestDrivers]
                bestDriver, (currLocToOrderPickup, totalDuration) = getBestDriver(map, delayedRemainingDrivers, order)
                rate = min(basePay, self.hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
                # NOTE: make this code a helper fxn?
                order.price = rate + order.additionalCompensation
                driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
                setOrderIntermediateDurations(map, driverReliabilityFactor, order, bestDriver.currLoc, order.pickup, order.dropoff)
                order.driverToPickupDur = order.intermediateEdges.getScaledPickupTime()
                order.pickupToDeliverDur = order.intermediateEdges.getScaledDeliverTime()
                bestDriver.addOrder(order)
                order.addDriver(bestDriver)

        self.delayedQueue = newDelayedQueue

    def orderStep(self, map, orderQueue, drivers, basePay, minute):
        self.checkDelayedOrders(map, minute, basePay)
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].releaseTime <= minute:
            currOrder = orderQueue[0]
            availableDrivers = getAvailableDrivers(drivers) 
            # can only assign order if there is an open driver
            if availableDrivers:
                currOrder = orderQueue.pop(0)
                self.assignDriver(map, availableDrivers, currOrder, minute, basePay)

            delayedQueueOrders = []
            for order, _, _ in self.delayedQueue:
                delayedQueueOrders.append(order)
            self.incDelayedInAsssignmentOrders(delayedQueueOrders + orderQueue, minute)




