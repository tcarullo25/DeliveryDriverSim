#TODO: make customers involved as well
class Order:
    def __init__(self, id, start, dest, duration, price):
        self.id = id
        self.loc = start
        self.dest = dest
        self.duration = duration
        self.price = price

class Driver:
    def __init__(self, id, startLoc):
        self.id = id
        self.currLoc = startLoc
        self.order = None
        self.earnings = 0
        self.totalOrders = 0
    
    def addOrder(self, order):
        self.order = order

