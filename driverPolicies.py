def greedy(driver, order, minute, currLocToOrderPickup, totalTime):
    return True

def rateFocused(driver, order, minute, currLocToOrderPickup, totalTime):
    desiredRate = 14
    currRate = order.price / (totalTime / 60)
    # order rate must be at least desired rate 
    return currRate >= desiredRate


# change currloctorderpicup and totaltime to behavior factored times
def reputationFocused(driver, order, minute, currLocToOrderPickup, totalTime):
    hasDecentReputation = driver.reputation >= 70
    # if driver is late to either pickup or delivery, must have decent reputation to accept order
    if minute + currLocToOrderPickup > order.pickupTime and not hasDecentReputation: return False
    if minute + totalTime > order.deliverTime and not hasDecentReputation: return False
    # otherwise accept order
    return True

# third one can be a hybrid of rateFocused and reputationfocused