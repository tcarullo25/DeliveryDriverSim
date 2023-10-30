from graphs import *
from ordersAndDrivers import * 
from tests import *
from visualizations import *
from driverPolicies import *
from companyPolicies import *
import copy

def driverDecide(drivers, durs, currOrder, minute):
    remainingDrivers = []
    for i in range(len(drivers)):
        driver = drivers[i]
        currLocToOrderDuration, totalTime = durs[i]
        # if driver policy accepts order add it to remaining drivers
        if driver.policy(driver, currOrder, minute, currLocToOrderDuration, totalTime):
            remainingDrivers.append(driver)
    return remainingDrivers

def initSim(map, orderQueue, drivers, basePay, totalMins):
    ordersCompleted = 0
    finishedOrders = []
    company = KBestDriversPolicy()

    for minute in range(totalMins):
        # ORDER LOGIC #
        company.orderStep(map, orderQueue, drivers, basePay, minute)

        # DRIVER LOGIC #
        for driver in drivers:
                if driver.order != None:
                    driver.checkOrder(minute)
                    # check if completed order and if so reflect driver's status
                    if driver.order.delivered:
                        ordersCompleted += 1
                        finishedOrders.append(driver.order)
                        driver.updateReputation()
                        driver.completeOrder()
                else:
                    driver.idleTime += 1
                    driver.nonproductiveTime += 1
                driver.reputationOverTime.append(driver.reputation)
                
    delayedOrders = company.finishSim()
    return drivers, (ordersCompleted, delayedOrders, finishedOrders)

def displayResults(drivers, orderInfo, totalMins):
    ordersCompleted, _, _ = orderInfo
    res = f'SEED: {seed}\nTEST: {testNum}\n'
    res += f'There was a total of {ordersCompleted} orders completed across all drivers.\nThe earnings for each driver are as follows:\n'
    sumOfRates = 0
    for driver in drivers:
        driver.earnings = round(driver.earnings, 2)
        driverRate = driver.earnings / (totalMins/60)
        sumOfRates += driverRate
        res += f'• Driver {driver.id} received ${driver.earnings}, completed {driver.totalOrders} orders and it took them {driver.totalOrderTime} timesteps with a reputation of {driver.reputation}.\n'
    avgRate = round(sumOfRates/len(drivers),2)
    res += f'The average wage across all drivers is: ${avgRate}/hr'
    print(res)
    displayVisualizations(drivers, orderInfo, avgRate, totalMins)

def chooseLayout(graphType, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins, drivers, basePay = eval(f'test{testNum}()')
    allOrders = copy.copy(orderQueue)
    driversStart = copy.copy(drivers)
    drivers, orderInfo = initSim(map, orderQueue, drivers, basePay, totalMins)
    map.displayGraphDrivers(driversStart)
    map.displayGraphOrders(allOrders) 
    displayResults(drivers, orderInfo, totalMins)

graphType = 'grid'
testNum = 9
seed = 2

#NOTE: seed dictates randomness of drivers' lateness
random.seed(seed)

chooseLayout(graphType, testNum)
