import math 
import random 
from driverHelperFns import *

class Order:
    def __init__(self, id, pickup, dropoff, releaseTime, pickupTime, deliverTime, price):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.releaseTime = releaseTime
        self.price = price
        self.pickupTime = pickupTime
        self.deliverTime = deliverTime
        self.driver = None
        self.pickedUp = False
        self.delivered = False
        self.intermediateEdges = OrderIntermediateEdges()
        self.lateToPickupDuration = 0 #late pickup and deliver durs accumulate only after driver assignment
        self.lateToDeliverDuration = 0
        self.delayedInAssignmentDuration = 0
        self.additionalCompensation = 0
        # all below will update when assigned to driver
        self.driverToPickupDur = 0 
        self.pickupToDeliverDur = 0
        self.timePickedUpAt = 0
    
    def addDriver(self, driver):
        self.driver = driver

class IntermediateEdges():
    def __init__(self):
        self.edges = []
        self.currIndex = 0

    def passMinute(self, driver):
        if self.currIndex >= len(self.edges): return
        n1, n2, w = self.edges[self.currIndex]
        self.edges[self.currIndex] = n1, n2, w - 1
        if w - 1 <= 0:
            self.currIndex += 1
            driver.currLoc = n2

class ClusterIntermediateEdges(IntermediateEdges):
    def __init__(self):
        super().__init__()   

class OrderIntermediateEdges(IntermediateEdges):
    def __init__(self):
        super().__init__()
        self.pickupEdges = []
        self.deliverEdges = []

    def initList(self, pickupEdges, deliverEdges):
        self.edges = pickupEdges + deliverEdges
        self.pickupEdges = pickupEdges 
        self.deliverEdges = deliverEdges
    
    def getScaledPickupTime(self):
        return sum(edge[2] for edge in self.pickupEdges)
    
    def getScaledDeliverTime(self):
        return sum(edge[2] for edge in self.deliverEdges)

class Driver:
    def __init__(self, id, startLoc, policy, behavior):
        self.id = id
        self.currLoc = startLoc
        self.policy = policy
        self.behavior = behavior
        self.order = None
        self.earnings = 0
        self.totalOrders = 0
        self.totalOrderTime  = 0
        self.currOrderTime = 0
        self.onTimeStreak = 0
        self.intermediateEdges = ClusterIntermediateEdges()
        self.targetedCluster = None
        self.clusterDur = None
        self.idleTime = 0 # occurs when the driver has no order assigned
        self.nonproductiveTime = 0 # idle time + time from driver loc to order pickup
        self.reputation = 100
        self.reputationOverTime = [] # list of reputations every min
        self.orderTimes = []
        self.latePickupOrders = []
        self.lateDeliverOrders = []
        self.latenessHistory = [] # stores bool for every order signifying if late or not
    
    def __str__(self):
        return f'Driver {self.id}'
    
    def addOrder(self, order):
        self.targetedCluster, self.clusterDur = None, None
        self.order = order
    
    def checkOrder(self, minute):
        self.currOrderTime += 1
        # have not arrived at restaurant yet
        if not self.order.pickedUp:
            self.nonproductiveTime += 1
            self.order.intermediateEdges.passMinute(self)
            self.order.driverToPickupDur -= 1
            # pickup time passed - increase late duration
            if self.order.pickupTime < minute:
                self.order.lateToPickupDuration += 1
        # have not delivered order yet
        if self.order.pickedUp and not self.order.delivered:
            self.order.intermediateEdges.passMinute(self)
            self.order.pickupToDeliverDur -= 1
            if self.order.pickupToDeliverDur <= 0:
                self.order.delivered = True
            # if time of pickup is past pickup time, shift deliver time by that difference
            if self.order.timePickedUpAt > self.order.pickupTime:
                stretchedDeliverTime = self.order.deliverTime + (self.order.timePickedUpAt - self.order.pickupTime)
            else:
                stretchedDeliverTime = self.order.deliverTime 
            # deliver time passed - increase late duration
            if stretchedDeliverTime <= minute:
                self.order.lateToDeliverDuration += 1
        # check if order was picked up last to avoid skipping a minute of the deliver dur
        if not self.order.pickedUp and self.order.driverToPickupDur <= 0:
            self.order.pickedUp = True
            self.order.timePickedUpAt = minute

    def moveToCluster(self, map, clusters):
        if self.targetedCluster == None:
            self.targetedCluster, self.clusterDur = getBestCluster(map, self.currLoc, clusters)
            setClusterIntermediateDurations(map, self)
        self.intermediateEdges.passMinute(self)       

    def completeOrder(self):
        if self.order.lateToPickupDuration:
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
        maxPenalty = 20
        maxLateness = 15 # driver will get the max penalty if lateness >= to this threshold
        base = maxLateness**(1/maxPenalty) # base to scale wrt maxLateness & maxPenalty
        gracePeriod = 2
        baseReward = 2
        frequencyPenaltyFactor = 0.5
       

        if self.order.lateToPickupDuration > gracePeriod or self.order.lateToDeliverDuration > gracePeriod:
            self.latenessHistory.append(True)
        else:
            self.latenessHistory.append(False)
        # keep track of the number of late orders from last 10 orders
        if len(self.latenessHistory) > 10:
            self.latenessHistory.pop(0)
        lateOrdersInWindow = self.latenessHistory.count(True)

        if self.order.lateToPickupDuration > 0:
            self.onTimeStreak = 0
        if self.order.lateToPickupDuration > gracePeriod: 
            # penalty is function of how late they + their lateness history
            individualPenalty = min(math.log(self.order.lateToPickupDuration, base), maxPenalty)
            frequencyPenalty = frequencyPenaltyFactor * math.log(lateOrdersInWindow + 1, base)
            self.reputation -= frequencyPenalty + individualPenalty
        elif not self.order.lateToPickupDuration:
            self.onTimeStreak += 1
            self.reputation += baseReward * math.log(self.onTimeStreak + 1)
        
        self.reputation = max(min(self.reputation, 100), 0)
        if self.order.lateToDeliverDuration > 0:
            self.onTimeStreak = 0
        if self.order.lateToDeliverDuration > gracePeriod:
            individualPenalty = min(math.log(self.order.lateToDeliverDuration, base), maxPenalty)
            frequencyPenalty = frequencyPenaltyFactor * math.log(lateOrdersInWindow + 1, base)
            self.reputation -= frequencyPenalty + individualPenalty
        elif not self.order.lateToDeliverDuration:
            self.onTimeStreak += 1
            self.reputation += baseReward * math.log(self.onTimeStreak + 1)

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
    
    def computeDriverReliabilityFactor(self, w1=0.10):
        # randomness allows driver to either be faster or slower than expected
        return self.behavior + w1 * random.uniform(-1, 1)
       
    
# change reliability factor function ^ preset behavior factor (1.1, 1.0, .9) + w2 * random.uniform(-1, 1)



# LATER:
#  compute awareness factor - take into account behavior factor (no randomness factor) * theoretical duration
#  awareness + reputation  

