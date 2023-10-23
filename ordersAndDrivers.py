import math 
import random 
class Order:
    def __init__(self, id, pickup, dropoff, releaseTime, pickupTime, deliverTime, price):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.releaseTime = releaseTime
        self.price = price
        self.pickupTime = pickupTime
        self.deliverTime = deliverTime
        self.pickedUp = False
        self.delivered = False
        self.lateToPickupDuration = 0
        self.lateToDeliverDuration = 0
        self.delayedInAssignmentDuration = 0
        # all below will update when assigned to driver
        self.driverToPickupDur = 0 
        self.pickupToDeliverDur = 0

class Driver:
    def __init__(self, id, startLoc):
        self.id = id
        self.currLoc = startLoc
        self.order = None
        self.earnings = 0
        self.totalOrders = 0
        self.totalOrderTime  = 0
        self.currOrderTime = 0
        self.idleTime = 0 # occurs when the driver has no order assigned
        self.nonproductiveTime = 0 # idle time + time from driver loc to order pickup
        self.reputation = 100
        self.reputationOverTime = [] # list of reputations every min
        self.orderTimes = []
        self.latePickupOrders = []
        self.lateDeliverOrders = []
    
    def addOrder(self, order):
        self.order = order
    
    def checkOrder(self, minute):
        self.currOrderTime += 1
        #NOTE: could mark late only after a certain amount of time? (e.g. after 10 mins driver will get penalized)

        # have not arrived at restaurant yet
        if not self.order.pickedUp:
            self.nonproductiveTime += 1
            self.order.driverToPickupDur -= 1
            if self.order.driverToPickupDur <= 0:
                self.order.pickedUp = True
            # pickup time passed - increase late duration
            if self.order.pickupTime < minute:
                self.order.lateToPickupDuration += 1
        # have not delivered order yet
        if self.order.pickedUp and not self.order.delivered:
            self.order.pickupToDeliverDur -= 1
            if self.order.pickupToDeliverDur <= 0:
                self.order.delivered = True
            # deliver time passed - increase late duration
            if self.order.deliverTime < minute:
                self.order.lateToDeliverDuration += 1

    def completeOrder(self):
        if self.order.lateToPickupDuration:
            #print(self.order.id, self.order.pickupTime, self.order.lateToPickupDuration)
            self.latePickupOrders.append(self.order)
        if self.order.lateToDeliverDuration:
            self.lateDeliverOrders.append(self.order)
        self.currLoc = self.order.dropoff
        self.earnings += self.order.price
        self.totalOrders += 1
        self.totalOrderTime += self.currOrderTime
        self.orderTimes.append(self.currOrderTime)
        self.currOrderTime = 0
        self.order = None
    
    def updateReputation(self):
        maxPenalty = 10
        maxLateness = 15 # driver will get the max penalty if lateness >= to this threshold
        epsilon = 1e-99 # in case lateness durations are 0
        base = (maxLateness + epsilon)**(1/maxPenalty) # base to scale wrt maxLateness & maxPenalty
        gracePeriod = 5

        if self.order.lateToPickupDuration > gracePeriod: 
            self.reputation -= min(math.log(self.order.lateToPickupDuration + epsilon, base), maxPenalty) 
        elif not self.order.lateToPickupDuration:
            self.reputation += maxPenalty
            print(self.order.lateToPickupDuration, min(math.log(maxLateness - self.order.lateToPickupDuration + epsilon, base), maxPenalty))

        self.reputation = max(min(self.reputation, 100), 0)

        if self.order.lateToDeliverDuration > gracePeriod:
            self.reputation -= min(math.log(self.order.lateToDeliverDuration + epsilon, base), maxPenalty)
        elif not self.order.lateToDeliverDuration:
            self.reputation += maxPenalty
            
        self.reputation = max(min(self.reputation, 100), 0)
        self.reputation = round(self.reputation, 2)

    def computeDriverOrderScore(self, currLocToOrderDuration, maxDuration, w1=40, w2=60):
        repScore = w1 * self.reputation/100
        if maxDuration == 0: # if furthest driver is 0 mins away
            durationScore = w2
        else:
            durationScore = w2 * (1 - currLocToOrderDuration / maxDuration)
        score = repScore + durationScore
        return score 
    
    def computeDriverReliabilityFactor(self, w1=0.25, w2=0.10):
        baseFactor = 1 + w1 * (1 - self.reputation/100)
        # randomness allowing driver to either be faster or slower than expected
        randomFactor = baseFactor * w2 * random.uniform(-1, 1)
        return baseFactor + randomFactor