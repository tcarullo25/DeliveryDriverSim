class Order:
    def __init__(self, id, pickup, dropoff, duration, timestep, price):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.duration = duration
        self.driverToPickupDur = 0 # will update when assigned to driver
        self.timestep = timestep
        self.price = price
        self.delayedLength = 0

class Driver:
    def __init__(self, id, startLoc):
        self.id = id
        self.currLoc = startLoc
        self.order = None
        self.earnings = 0
        self.totalOrders = 0
        self.totalOrderTime  = 0
        self.currOrderTime = 0
        self.idleTime = 0 # when the driver has no order assigned
        self.nonproductiveTime = 0 # idle time + time from driver loc to order pickup
        self.orderTimes = []
    
    def addOrder(self, order):
        self.order = order

