class DriverPolicy():
    def __init__(self, policyName, policyFn, clusterHover):
        self.policyName = policyName
        self.policyFn = policyFn
        self.clusterHover = clusterHover

    def __str__(self):
        return self.policyName

def greedy(driver, order, minute, currLocToOrderPickup, totalTime):
    return True

def rateFocused(driver, order, minute, currLocToOrderPickup, totalTime):
    desiredRate = 14
    
    orderPrice = order.price + order.additionalCompensation
    currRate = orderPrice / (totalTime / 60)
    # order rate must be at least desired rate 
    return currRate >= desiredRate

def reputationFocused(driver, order, minute, currLocToOrderPickup, totalTime):
    hasDecentReputation = driver.reputation >= 80
    # if driver is late to either pickup or delivery, must have decent reputation to accept order

    if minute + currLocToOrderPickup > order.pickupTime and not hasDecentReputation: 
        return False
    if minute + totalTime > order.deliverTime and not hasDecentReputation: 
        return False
    # otherwise accept order
    return True

# create a new driver policy that is a hybrid/combination of rateFocused and reputationFocused 

# group of driver stats by policies


# run samew simulaiton all for each policy to create baseline
