from graphs import *
from ordersAndDrivers import * 
from tests import *
from visualizations import *
from driverPolicies import *
from companyPolicies import *
import copy

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
                
    delayedOrders, driverLog = company.finishSim()
    return drivers, (ordersCompleted, delayedOrders, finishedOrders, driverLog)

def displayResults(drivers, orderInfo, totalMins):
    ordersCompleted, _, _, _ = orderInfo
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

def displayOrderRoutes(map, driverLog, allOrders):
    print(f"All completed orders: {[order.id for order in allOrders if order.driver]}")
    print(f"All incompleted orders: {[order.id for order in allOrders if order.driver == None]}")

    while True:
        userInput = input("Please select a completed order from the above list. To see a select list of orders completed throughout the simulation, type 'L'.\nWhen you have finished, please type 'Q'.\n")
        if userInput.upper() == 'Q': 
            break
        if userInput.upper() == 'L':
            for i in range(0, len(allOrders), 10):
                map.displayOrderRoute(driverLog, allOrders[i])
        id = int(userInput)
        order = None
        for currOrder in allOrders:
            if currOrder.id == id:
                order = currOrder
        map.displayOrderRoute(driverLog, order)

def chooseLayout(graphType, testNum):
    if graphType == 'grid':
        map, orderQueue, totalMins, drivers, basePay = eval(f'test{testNum}()')
    allOrders = copy.copy(orderQueue)
    driversStart = copy.copy(drivers)
    drivers, orderInfo = initSim(map, orderQueue, drivers, basePay, totalMins)
    _, _, _, driverLog = orderInfo
    displayOrderRoutes(map, driverLog, allOrders)
    map.displayGraphDrivers(driversStart)
    map.displayGraphOrders(allOrders) 
    displayResults(drivers, orderInfo, totalMins)

graphType = 'grid'
testNum = 2
seed = 2

#NOTE: seed dictates randomness of drivers' reliability (lateness)
random.seed(seed)

chooseLayout(graphType, testNum)