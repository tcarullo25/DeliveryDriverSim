#TODO: make customers involved as well
class Order:
    def __init__(self, id, start, dest, duration, timestep, price):
        self.id = id
        self.loc = start
        self.dest = dest
        self.duration = duration
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
        self.idleTime = 0
        self.orderTimes = []
    
    def addOrder(self, order):
        self.order = order

