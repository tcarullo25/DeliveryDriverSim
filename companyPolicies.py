from driverHelperFns import *
import math

## COMPANY INTERFACE ##
class Company():
    def __init__(self):
        self.delayedOrders = 0
        self.hourlyRate = 25
    
    def orderStep(self, map, orderQueue, drivers, basePay, totalMins):
        pass

    def incDelayedInAsssignmentOrders(self, orderQueue, minute):
        for order in orderQueue:
            if order.releaseTime < minute:
                if order.delayedInAssignmentDuration == 0:
                    self.delayedOrders += 1
                order.delayedInAssignmentDuration += 1

    def finishSim(self):
        return self.delayedOrders
    
class SelectiveBroadPolicy(Company):
    def assignDriver(self, map, drivers, currOrder, minute, basePay):
        bestDrivers, bestDurs = getKBestDrivers(map, drivers, currOrder)
        # see who accepts 
        remainingDrivers = driverDecide(bestDrivers, bestDurs, currOrder, minute)
        if not remainingDrivers:
            # if nobody accepted, send it out to all drivers
            # NOTE: there will usually need to be a large amount of drivers in test case for this to always work
            availableDrivers, allDurs = getKBestDrivers(map, drivers, currOrder, k=len(drivers))
            remainingDrivers = driverDecide(availableDrivers, allDurs, currOrder, minute)
        # get the best driver out of the previous best drivers who accepted order
        #NOTE: the best driver will be in terms of JUST the remaining drivers (the max duration likely changed), 
        # so the answer may slightly vary from what the single-most best driver was before
        bestDriver, (currLocToOrderPickup, totalDuration) = getBestDriver(map, remainingDrivers, currOrder)
        # the order's price will be the lower of base pay or rate calculated from pickup to dropoff duration
        # NOTE: are we sure we dont want to add the rate to base pay?
        rate = min(basePay, self.hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
        currOrder.price = rate
        driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
        currOrder.driverToPickupDur = currLocToOrderPickup * driverReliabilityFactor
        pickupToDeliverDur = totalDuration - currLocToOrderPickup
        currOrder.pickupToDeliverDur = pickupToDeliverDur * driverReliabilityFactor
        bestDriver.addOrder(currOrder)

    def orderStep(self, map, orderQueue, drivers, basePay, minute):
        # peek at next order in queue to see if it's ready to release
        if orderQueue and orderQueue[0].releaseTime <= minute:
            currOrder = orderQueue[0]
            availableDrivers = getAvailableDrivers(drivers)
            # can only assign order if there is an open driver
            if availableDrivers:
                currOrder = orderQueue.pop(0)
                self.assignDriver(map, availableDrivers, currOrder, minute, basePay)
            self.incDelayedInAsssignmentOrders(orderQueue, minute)

class KBestDriversPolicy(Company):
    def __init__(self):
        super().__init__()
        self.delayedQueue = []

    def assignDriver(self, map, drivers, currOrder, minute, basePay):
        bestDrivers, bestDurs = getKBestDrivers(map, drivers, currOrder)
        # see who accepts 
        remainingDrivers = driverDecide(bestDrivers, bestDurs, currOrder, minute)
        if not remainingDrivers:
            # add bestDrivers and the currOrder to a delayedQueue
            # check delayedQueue before orderQueue - check if nonempty
            # if so increment order price and run driverDecide again
            currOrder.price += 1
            self.delayedQueue.append((currOrder, bestDrivers, bestDurs))
        else:
        # get the best driver out of the previous best drivers who accepted order
        #NOTE: the best driver will be in terms of JUST the remaining drivers (the max duration likely changed), 
        # so the answer may slightly vary from what the single-most best driver was before
            bestDriver, (currLocToOrderPickup, totalDuration) = getBestDriver(map, remainingDrivers, currOrder)
            # the order's price will be the lower of base pay or rate calculated from pickup to dropoff duration
            # NOTE: are we sure we dont want to add the rate to base pay?
            rate = min(basePay, self.hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
            currOrder.price = rate
            driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
            currOrder.driverToPickupDur = currLocToOrderPickup * driverReliabilityFactor  
            pickupToDeliverDur = totalDuration - currLocToOrderPickup
            currOrder.pickupToDeliverDur = pickupToDeliverDur * driverReliabilityFactor
            bestDriver.addOrder(currOrder)

    def checkDelayedOrders(self, map, minute, basePay):
        newDelayedQueue = []
        for (order, bestDrivers, bestDurs) in self.delayedQueue:
            # get the best drivers for the given order and check who is still available 
            delayedBestDrivers = getAvailableDrivers(bestDrivers) 
            delayedRemainingDrivers = driverDecide(delayedBestDrivers, bestDurs, order, minute)
            # if no driver still does not want to take it, add order back to queue
            if not delayedRemainingDrivers:
                order.price += 1
                newDelayedQueue.append((order, delayedBestDrivers, bestDurs))
            else:
                bestDriver, (currLocToOrderPickup, totalDuration) = getBestDriver(map, delayedRemainingDrivers, order)
                rate = min(basePay, self.hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
                additionalCompensation = order.price - basePay
                order.price = rate + additionalCompensation
                driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
                order.driverToPickupDur = math.ceil(currLocToOrderPickup * driverReliabilityFactor)
                pickupToDeliverDur = totalDuration - currLocToOrderPickup
                order.pickupToDeliverDur = math.ceil(pickupToDeliverDur * driverReliabilityFactor) 
                bestDriver.addOrder(order)

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




