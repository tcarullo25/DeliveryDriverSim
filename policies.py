def greedy(driver, order, minute, currLocToOrderPickup, totalTime):
    return True

def rateFocused(driver, order, minute, currLocToOrderPickup, totalTime):
    desiredRate = 18
    currRate = order.price / (totalTime / 60)
    # order rate must be at least desired rate 
    return currRate >= desiredRate

def reputationFocused(driver, order, minute, currLocToOrderPickup, totalTime):
    decentReputation = driver.reputation >= 65
    # if driver is late to either pickup or delivery, must have decent reputation to accept order
    if minute + currLocToOrderPickup > order.pickupTime and not decentReputation: return False
    if minute + totalTime > order.deliverTime and not decentReputation: return False
    # otherwise accept order
    return True




    

