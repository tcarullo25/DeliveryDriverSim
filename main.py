from graphs import *
from ordersAndDrivers import * 
from tests import *
from visualizations import *
from driverPolicies import *
from companyPolicies import *
from cmu_graphics import *
import random
import copy

def initSim(map, clusters, orderQueue, drivers, basePay, totalMins):
    ordersCompleted = 0
    finishedOrders = []
    company = KBestDriversPolicy(clusters, map, totalMins)
    for minute in range(totalMins):
        # ORDER LOGIC #
        company.orderStep(map, orderQueue, drivers, basePay, minute)

        # DRIVER LOGIC #
        for driver in drivers:
                if driver.order != None:
                    driver.checkOrder(minute)
                    orderInfo = (driver.order, driver.order.price)
                    # check if completed order and if so reflect driver's status
                    if driver.order.delivered:
                        ordersCompleted += 1
                        finishedOrders.append(driver.order)
                        driver.updateReputation()
                        driver.completeOrder()
                    
                else:
                    if driver.policy.clusterHover:
                        driver.moveToCluster(map, company.clusters)
                    driver.idleTime += 1
                    driver.nonproductiveTime += 1
                    orderInfo = (None, None)

                company.driverLog[minute] = [[driver.id, driver.currLoc, orderInfo, driver.earnings, driver.reputation] for driver in drivers]
                # wont need this reputation over time because of driver log
                driver.reputationOverTime.append(driver.reputation)            
    delayedOrders, orderLog, driverLog = company.finishSim()
    return drivers, (ordersCompleted, delayedOrders, finishedOrders, orderLog, driverLog)

def displayResults(drivers, orderInfo, totalMins):
    ordersCompleted, _, _, _ = orderInfo
    res = f'SEED: {seed}\nTEST: {testNum}\n'
    res += f'There was a total of {ordersCompleted} orders completed across all drivers.\nThe earnings for each driver are as follows:\n'
    sumOfRates = sumOfRatesActiveTime = 0
    for driver in drivers:
        driver.earnings = round(driver.earnings, 2)
        driverRate = driver.earnings / (totalMins/60)
        driverRateActiveTime = driver.earnings / (driver.totalOrderTime/60)
        sumOfRates += driverRate
        sumOfRatesActiveTime += driverRateActiveTime
        res += f'• Driver {driver.id} received ${driver.earnings}, completed {driver.totalOrders} orders and it took them {driver.totalOrderTime} timesteps with a reputation of {driver.reputation}.\n'
    avgRate = round(sumOfRates/len(drivers),2)
    avgRateActiveTime = round(sumOfRatesActiveTime/len(drivers), 2)
    res += f'The average wage across all drivers is: ${avgRate}/hr\nThe average wage across all drivers counting only their active time is ${avgRateActiveTime}/hr'
    print(res)
    displayVisualizations(drivers, orderInfo, avgRate, avgRateActiveTime, totalMins)

def displayOrderRoutes(map, orderLog, allOrders):
    print(f"All completed orders: {[order.id for order in allOrders if order.driver]}")
    print(f"All incompleted orders: {[order.id for order in allOrders if order.driver == None]}")

    while True:
        userInput = input("Please select a completed order from the above list. To see a select list of orders completed throughout the simulation, type 'L'.\nWhen you have finished, please type 'Q'.\n")
        if userInput.upper() == 'Q': 
            break
        if userInput.upper() == 'L':
            for i in range(0, len(allOrders), 10):
                map.displayOrderRoute(orderLog, allOrders[i])
        id = int(userInput)
        order = None
        for currOrder in allOrders:
            if currOrder.id == id:
                order = currOrder
        map.displayOrderRoute(orderLog, order)
def chooseLayout(testNum):
    map, clusters, orderQueue, totalMins, drivers, basePay = eval(f'test{testNum}()')
    allOrders = copy.copy(orderQueue)
    driversStart = copy.copy(drivers)
    drivers, orderInfo = initSim(map, clusters, orderQueue, drivers, basePay, totalMins)
    _, _, _, orderLog, driverLog = orderInfo
    #displayOrderRoutes(map, orderLog, allOrders)
    #map.displayGraphOrders(allOrders) 
    #map.displayGraphDrivers(driversStart)
    #displayResults(drivers, orderInfo, totalMins)
    return map, clusters, orderQueue, totalMins, drivers, basePay, driverLog, allOrders

#https://academy.cs.cmu.edu/exercise/11953
def onAppStart(app):
    map, clusters, orderQueue, totalMins, drivers, basePay, driverLog, allOrders = chooseLayout(testNum)
    app.driverColors = ['red', 'orange', 'blue', 'violet', 'yellow', 'purple', 'brown', 'green']
    app.clusters = clusters
    app.orderQueue = orderQueue
    app.orders = allOrders
    app.totalMins = totalMins
    app.drivers = drivers
    app.basePay = basePay
    app.driverLog = driverLog
    app.rows = map.n
    app.cols = map.m
    app.grid = map.adjMatrix
    app.margin = 50
    app.currMin = 0
    app.stepsPerSecond = 60

#def onStep(app):
#    if app.currMin < app.totalMins - 1:
#        app.currMin += 1
def onKeyPress(app, key):
    if key.lower() == 'up':
        app.currMin += 1
    if key.lower() == 'down':
        app.currMin -= 1

def redrawAll(app):
    drawGrid(app)
    drawLabel(f'Current Minute: {app.currMin}', 2*app.margin, app.margin//2, size = 15)

def drawGrid(app):
    currLog = app.driverLog[app.currMin]
    for row in range(app.rows):
        for col in range(app.cols):
            cell = col + app.cols * row
            color = ''
            text = ''
            for order in app.orders:
                if order.pickup == cell:
                    color = 'darkRed'
                    text = order.id
                elif order.dropoff == cell:
                    color = 'darkGreen'
                    text = order.id
            drawCell(app, row, col, color if color != '' else None, text)
            count = 0
            color = ''
            ids = []
            for i in range(len(app.drivers)):
                driverLoc = currLog[i][1]
                if driverLoc == cell:
                    color += app.driverColors[currLog[i][0] % len(app.driverColors)] + ' '
                    count += 1
                    ids.append(currLog[i][0])
            if count > 0:
                drawDriver(app, row, col, color[:-1].split() if color != '' else None, count, ids)
            
def drawDriver(app, row, col, colors, count, ids):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    cx = cellLeft + cellWidth//(2**count)
    cy = cellTop + cellHeight//(2**count)
    circlesPerRow = int(count**0.5)
    if circlesPerRow**2 < count:
        circlesPerRow += 1
    padding = 5
    diameter = min(cellWidth, cellHeight) / circlesPerRow - 2 * padding
    radius = diameter / 2
    for i in range(count):
        rowNumber = i // circlesPerRow
        colNumber = i % circlesPerRow
        cx = cellLeft + colNumber * (diameter + 2 * padding) + radius + padding
        cy = cellTop + rowNumber * (diameter + 2 * padding) + radius + padding
        drawCircle(cx, cy, radius, fill=colors[i])
        drawLabel(ids[i], cx, cy, size = 30 if count == 1 else 15)

def drawCell(app, row, col, color, text):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black')
    drawLabel(text, cellLeft + cellWidth//2, cellTop + cellHeight//2, size = 30)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.margin + col * cellWidth
    cellTop = app.margin + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = (app.width - 2*app.margin) / app.cols
    cellHeight = (app.height - 2*app.margin) / app.rows
    return (cellWidth, cellHeight)


testNum = 2
seed = 2
#NOTE: seed dictates randomness of drivers' reliability (lateness)
random.seed(seed)
runApp(800, 800)