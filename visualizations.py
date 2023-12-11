import matplotlib.pyplot as plt
import mplcursors
import numpy as np

def displayVisualizations(drivers, orderInfo, avgRate, totalMins):
    ordersCompleted, delayedOrders, finishedOrders, _ = orderInfo
    plotAllReputationsOverTime(drivers, totalMins)
    plotAvgReputationOverTime(drivers, totalMins)
    plotReputation(drivers)
    plotLatePickupsDeliveries(drivers)
    plotDriversLateOrders(drivers)
    plotDriverEarnings(drivers, avgRate)
    plotOrderTimes(drivers)
    plotOrdersPerDriver(drivers)
    plotDeliveryDurations(drivers)
    plotIdleTimes(drivers)
    plotNonproductiveTime(drivers)
    plotDelayedOrders(ordersCompleted, delayedOrders)
    allOrders = [driver.order for driver in drivers if driver.order] + finishedOrders
    plotOrderLateToPickUpDurations(allOrders)
    plotOrderLateToDeliverDurations(allOrders)
    plotOrderDelayInAssignmentDurations(allOrders)
    
def plotDriverEarnings(drivers, avgRate):
    earnings = [driver.earnings for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.scatter(driverIDs, earnings, color='blue', label='Earnings')
    avgEarning = np.mean(earnings)
    plt.axhline(avgEarning, color='red', linestyle='dashed', linewidth=2, label="Avg Earning")
    plt.title(f'{drivers[0].policy}: Driver Earnings\n(Average Rate: ${avgRate}/hr)')
    plt.xlabel('Driver ID')
    plt.xticks(np.arange(min(driverIDs), max(driverIDs) + 1, 1.0))
    plt.ylabel('Earnings ($)')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    #plt.show()
    plt.savefig('Driver Earnings')
    plt.clf()

def plotOrderTimes(drivers):
    orderTimes = [time for driver in drivers for time in driver.orderTimes]
    orderIDs = list(range(len(orderTimes)))

    plt.scatter(orderIDs, orderTimes, color='blue')
    plt.title(f'{drivers[0].policy}: Time Taken for Each Order')
    plt.xlabel('Order ID')
    plt.ylabel('Time (minutes)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    #plt.show()
    plt.savefig('Order Times')
    plt.clf()

def plotOrdersPerDriver(drivers):
    orders = [driver.totalOrders for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.scatter(driverIDs, orders, color='blue')
    plt.title(f'{drivers[0].policy}: Number of Orders per Driver')
    plt.xlabel('Driver ID')
    plt.xticks(np.arange(min(driverIDs), max(driverIDs) + 1, 1.0))
    plt.ylabel('Number of Orders')
    plt.yticks(np.arange(min(orders), max(orders) + 1, 1.0))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    #plt.show()
    plt.savefig('Orders per Driver')
    plt.clf()

def plotDeliveryDurations(drivers):
    deliveryTimes = [time for driver in drivers for time in driver.orderTimes]

    plt.hist(deliveryTimes, bins=30, edgecolor='black', alpha=0.7)
    plt.title(f'{drivers[0].policy}: Distribution of Delivery Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Number of Deliveries')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    #plt.show()
    plt.savefig('Delivery Durations')
    plt.clf()

def plotIdleTimes(drivers):
    idleTimes = [driver.idleTime for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.bar(driverIDs, idleTimes, color='blue', alpha=0.7)
    plt.title(f'{drivers[0].policy}: Idle Times for Each Driver')
    plt.xlabel('Driver ID')
    plt.ylabel('Idle Time (minutes)')
    plt.xticks(driverIDs)  # To ensure every driver ID is shown on the x-axis
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    #plt.show()
    plt.savefig('Idle Times')
    plt.clf()

def plotNonproductiveTime(drivers):
    nonproductiveTimes = [driver.nonproductiveTime for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.bar(driverIDs, nonproductiveTimes, color='blue', alpha=0.7)
    plt.title(f'{drivers[0].policy}: Non-Productive Times for Each Driver')
    plt.xlabel('Driver ID')
    plt.ylabel('Non-Productive (minutes)')
    plt.xticks(driverIDs)  # To ensure every driver ID is shown on the x-axis
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    #plt.show()
    plt.savefig('Nonproductive Times')
    plt.clf()

def plotDelayedOrders(totalOrders, delayedOrders):
    fulfilledImmediately = totalOrders - delayedOrders
    labels = ['Fulfilled Immediately', 'Delayed']
    sizes = [fulfilledImmediately, delayedOrders]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['green', 'red'])
    plt.title('Proportion of Delayed in Asssignment Orders')
    plt.tight_layout()
    #plt.show()
    plt.savefig('Delayed Orders')
    plt.clf()

def plotOrderDelayInAssignmentDurations(orders):
    delays = [order.delayedInAssignmentDuration for order in orders if order.delayedInAssignmentDuration > 0]  
    if not delays:  
        plt.xlabel('Delay Duration (in timesteps)')
        plt.ylabel('Number of Orders')
        plt.title('Distribution of Order Delay in Assignment Durations')
        plt.show()  
        return  
    plt.hist(delays, bins=range(1, max(delays) + 2), align='left', rwidth=0.8, 
                                            color='skyblue', edgecolor='black')
    plt.xlabel(f'{orders[0].driver.policy}: Delay Duration (in timesteps)')
    plt.xticks(np.arange(min(delays), max(delays) + 1, 1.0))
    plt.ylabel('Number of Orders')
    plt.title(f'{orders[0].driver.policy}: Distribution of Order Delay in Assignment Durations')
    #plt.show()
    plt.savefig('Order Delay in Assignment Durations')
    plt.clf()

def plotOrderLateToPickUpDurations(orders):
    delays = [order.lateToPickupDuration for order in orders]  
    plt.hist(delays, bins=range(1, max(delays) + 2), align='left', rwidth=0.8, 
                                            color='skyblue', edgecolor='black')
    plt.xlabel(f'{orders[0].driver.policy}: Delay Duration (in timesteps)')
    plt.xticks(np.arange(min(delays), max(delays) + 1, 1.0))
    plt.ylabel('Number of Orders')
    plt.title(f'{orders[0].driver.policy}: Distribution of Order Late to Pickup Durations')
    #plt.show()
    plt.savefig('Order Late to Pickup Durations')
    plt.clf()

def plotOrderLateToDeliverDurations(orders):
    delays = [order.lateToDeliverDuration for order in orders]  
    plt.hist(delays, bins=range(1, max(delays) + 2), align='left', rwidth=0.8, 
                                            color='skyblue', edgecolor='black')
    plt.xlabel(f'{orders[0].driver.policy}: Delay Duration (in timesteps)')
    plt.xticks(np.arange(min(delays), max(delays) + 1, 1.0))
    plt.ylabel('Number of Orders')
    plt.title(f'{orders[0].driver.policy}: Distribution of Order Late to Deliver Durations')
    #plt.show()
    plt.savefig('Order Late to Deliver Durations')
    plt.clf()

def plotLatePickupsDeliveries(drivers):
    driverIds = [driver.id for driver in drivers]
    latePickups = [100 * len(driver.latePickupOrders)/driver.totalOrders for driver in drivers]
    lateDeliveries = [100 * len(driver.lateDeliverOrders)/driver.totalOrders for driver in drivers]
    
    bar_width = 0.35
    r1 = np.arange(len(driverIds))
    r2 = [x + bar_width for x in r1]

    plt.bar(r1, latePickups, color='b', width=bar_width, edgecolor='grey', label='Late Pickups')
    plt.bar(r2, lateDeliveries, color='r', width=bar_width, edgecolor='grey', label='Late Deliveries')
    
    plt.xlabel('Drivers', fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(len(driverIds))], driverIds)
    plt.ylabel('Number of Orders (%)', fontweight='bold', fontsize=15)
    plt.legend()
    
    plt.title(f'{drivers[0].policy}: Late Pickups and Deliveries per Driver')
    #plt.show()
    plt.savefig('Late Pickups and Deliveries')
    plt.clf()

def plotDriversLateOrders(drivers):
    driverIds = [driver.id for driver in drivers]
    totalLatePickupDurs = [sum(order.lateToPickupDuration for order in driver.latePickupOrders) for driver in drivers]
    totalLateDeliverDurs = [sum(order.lateToDeliverDuration for order in driver.lateDeliverOrders) for driver in drivers]

    bar_width = 0.25
    r1 = np.arange(len(driverIds))
    r2 = [x + bar_width for x in r1]

    plt.bar(r1, totalLatePickupDurs, color='b', width=bar_width, edgecolor='grey', label='Total Late to Pickup Duration')
    plt.bar(r2, totalLateDeliverDurs, color='r', width=bar_width, edgecolor='grey', label='Total Late to Deliver Duration')

    plt.xlabel('Drivers', fontweight='bold', fontsize=15)
    plt.ylabel('Total Time', fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(len(driverIds))], driverIds)
    plt.legend()

    plt.title(f'{drivers[0].policy}: Late Order Durations')
    #plt.show()
    plt.savefig('Drivers Late Orders')
    plt.clf()

def plotReputation(drivers):
    reputations = [driver.reputation for driver in drivers]

    plt.figure(figsize=(10, 5))
    plt.hist(reputations, bins=20, color='blue', edgecolor='black')
    plt.title(f'{drivers[0].policy}: Distribution of Driver Reputations')
    plt.xlabel('Reputation')
    plt.ylabel('Number of Drivers')
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    #plt.show()
    plt.savefig('Driver Reputations')
    plt.clf()

def plotAvgReputationOverTime(drivers, totalMins):
    avgReputations = []

    for minute in range(totalMins):
        totalRepAtMin = sum(driver.reputationOverTime[minute] for driver in drivers)
        avgRepAtMin = totalRepAtMin / len(drivers)
        avgReputations.append(avgRepAtMin)
    
    plt.plot(range(totalMins), avgReputations, color='blue', label='Average Reputation')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Average Reputation')
    plt.title(f'{drivers[0].policy}: Average Driver Reputation Over Time')
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.legend()
    #plt.show()
    plt.savefig('Average Reputation Over Time')
    plt.clf()

def plotAllReputationsOverTime(drivers, totalMins):
    plt.figure(figsize=(15, 7))

    for driver in drivers:
        plt.plot(range(totalMins), driver.reputationOverTime, label=f'Driver {driver.id}')

    plt.xlabel('Time (minutes)')
    plt.ylabel('Reputation')
    plt.title(f'{drivers[0].policy}: Driver Reputation Over Time')
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper right', fontsize='small', ncol=2)
    #plt.show()
    plt.savefig('All Reputations Over Time')
    plt.clf()