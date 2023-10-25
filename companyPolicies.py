from driverHelperFns import *
import math

# TEST JUST THIS CLASS OUT WITH MAIN AND SEE IF YOU GET SAME RESULTS WITHOUT USING THIS CLASS 

class KBestDriversPolicy():
    def __init__(self):
        self.delayedQueue = []

    def getKBestDrivers(self, map, drivers, currOrder, k=5):
        best = []
        maxDuration = getFurthestDriverDuration(map, drivers, currOrder)
        for driver in drivers:
            currLocToOrderDuration, totalTime = getOrderDuration(map, driver.currLoc, currOrder.pickup, currOrder.dropoff)
            score = driver.computeDriverOrderScore(currLocToOrderDuration, maxDuration)
            best.append((driver, score, (currLocToOrderDuration, totalTime)))

        bestSorted = sorted(best, key=lambda x: x[1], reverse=True)
        bestSorted = bestSorted[:k]
        bestDrivers = []
        bestDurs = []
        
        for driver, _, (currLocToOrderDuration, totalTime) in bestSorted:
            bestDrivers.append(driver)
            bestDurs.append((currLocToOrderDuration, totalTime))
        return bestDrivers, bestDurs

    def assignDriver(self, map, drivers, currOrder, minute, basePay, hourlyRate):
        bestDrivers, bestDurs = self.getKBestDrivers(map, drivers, currOrder)
        # see who accepts 
        #NOTE: what if nobody accepts????
        remainingDrivers = driverDecide(bestDrivers, bestDurs, currOrder, minute)
        if not remainingDrivers:
            # add bestDrivers and the currOrder to a delayedQueue
            # check delayedQueue before orderQueue - check if nonempty
            # if so increment order price and run driverDecide again
            currOrder.price += 1
            self.delayedQueue.append((currOrder, bestDrivers, bestDurs))
        else:
        # get the best driver out of the previous best who accepted order
        #NOTE: the best driver will be in terms of JUST the remaining drivers (the max duration likely changed), 
        # so the answer may slightly vary from what the single-most best driver was before
            bestDriver, (currLocToOrderPickup, totalDuration) = self.getBestDriver(map, remainingDrivers, currOrder)
            # the order's price will be the lower of base pay or rate calculated from pickup to dropoff duration
            # NOTE: are we sure we dont want to add the rate to base pay?
            rate = min(basePay, hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
            currOrder.price = rate
            driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
            currOrder.driverToPickupDur = currLocToOrderPickup * driverReliabilityFactor
            pickupToDeliverDur = totalDuration - currLocToOrderPickup
            currOrder.pickupToDeliverDur = pickupToDeliverDur * driverReliabilityFactor
            bestDriver.addOrder(currOrder)

    def checkDelayedOrders(self, map, minute, basePay, hourlyRate):
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
                rate = min(basePay, hourlyRate * ((totalDuration - currLocToOrderPickup)/60))
                additionalCompensation = order.price - basePay
                order.price = rate + additionalCompensation
                driverReliabilityFactor = bestDriver.computeDriverReliabilityFactor()
                order.driverToPickupDur = math.ceil(currLocToOrderPickup * driverReliabilityFactor)
                pickupToDeliverDur = totalDuration - currLocToOrderPickup
                order.pickupToDeliverDur = math.ceil(pickupToDeliverDur * driverReliabilityFactor) 
                bestDriver.addOrder(order)

        self.delayedQueue = newDelayedQueue
