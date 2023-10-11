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
        self.orderTimes = []
        self.latePickupOrders = []
        self.lateDeliverOrders = []
    
    def addOrder(self, order):
        self.order = order

