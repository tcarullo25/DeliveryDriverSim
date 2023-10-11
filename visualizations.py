import matplotlib.pyplot as plt
import mplcursors
import numpy as np

def displayVisualizations(drivers, orderInfo, avgRate):
    ordersCompleted, delayedOrders, finishedOrders = orderInfo
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
    plotOrderDelayDurations(allOrders)
    
def plotDriverEarnings(drivers, avgRate):
    earnings = [driver.earnings for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.scatter(driverIDs, earnings, color='blue', label='Earnings')
    avgEarning = np.mean(earnings)
    plt.axhline(avgEarning, color='red', linestyle='dashed', linewidth=2, label="Avg Earning")
    plt.title(f'Driver Earnings\n(Average Rate: ${avgRate}/hr)')
    plt.xlabel('Driver ID')
    plt.xticks(np.arange(min(driverIDs), max(driverIDs) + 1, 1.0))
    plt.ylabel('Earnings ($)')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    plt.show()

def plotOrderTimes(drivers):
    orderTimes = [time for driver in drivers for time in driver.orderTimes]
    orderIDs = list(range(len(orderTimes)))

    plt.scatter(orderIDs, orderTimes, color='blue')
    plt.title('Time Taken for Each Order')
    plt.xlabel('Order ID')
    plt.ylabel('Time (minutes)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    plt.show()

def plotOrdersPerDriver(drivers):
    orders = [driver.totalOrders for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.scatter(driverIDs, orders, color='blue')
    plt.title('Number of Orders per Driver')
    plt.xlabel('Driver ID')
    plt.xticks(np.arange(min(driverIDs), max(driverIDs) + 1, 1.0))
    plt.ylabel('Number of Orders')
    plt.yticks(np.arange(min(orders), max(orders) + 1, 1.0))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    plt.show()

def plotDeliveryDurations(drivers):
    deliveryTimes = [time for driver in drivers for time in driver.orderTimes]

    plt.hist(deliveryTimes, bins=30, edgecolor='black', alpha=0.7)
    plt.title('Distribution of Delivery Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Number of Deliveries')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

def plotIdleTimes(drivers):
    idleTimes = [driver.idleTime for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.bar(driverIDs, idleTimes, color='blue', alpha=0.7)
    plt.title('Idle Times for Each Driver')
    plt.xlabel('Driver ID')
    plt.ylabel('Idle Time (minutes)')
    plt.xticks(driverIDs)  # To ensure every driver ID is shown on the x-axis
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
def plotNonproductiveTime(drivers):
    nonproductiveTimes = [driver.nonproductiveTime for driver in drivers]
    driverIDs = [driver.id for driver in drivers]

    plt.bar(driverIDs, nonproductiveTimes, color='blue', alpha=0.7)
    plt.title('Non-Productive Times for Each Driver')
    plt.xlabel('Driver ID')
    plt.ylabel('Non-Productive (minutes)')
    plt.xticks(driverIDs)  # To ensure every driver ID is shown on the x-axis
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

def plotDelayedOrders(totalOrders, delayedOrders):
    fulfilledImmediately = totalOrders - delayedOrders
    labels = ['Fulfilled Immediately', 'Delayed']
    sizes = [fulfilledImmediately, delayedOrders]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['green', 'red'])
    plt.title('Proportion of Delayed in Asssignment Orders')
    plt.tight_layout()
    plt.show()

def plotOrderDelayDurations(orders):
    delays = [order.delayedInAssignmentDuration for order in orders if order.delayedInAssignmentDuration > 0]  
    plt.hist(delays, bins=range(1, max(delays) + 2), align='left', rwidth=0.8, 
                                            color='skyblue', edgecolor='black')
    plt.xlabel('Delay Duration (in timesteps)')
    plt.xticks(np.arange(min(delays), max(delays) + 1, 1.0))
    plt.ylabel('Number of Orders')
    plt.title('Distribution of Order Delay Durations')
    plt.show()

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
    
    plt.title('Late Pickups and Deliveries per Driver')
    plt.show()

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

    plt.title('Late Order Durations')
    plt.show()