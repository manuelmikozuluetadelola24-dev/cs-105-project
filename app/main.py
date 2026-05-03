import db

connection = db.initializeConnection(*(db.getConfig()))
db.filterDeliveriesStatusDelivered(connection)
print("\n\n")
connection = db.initializeConnection(*(db.getConfig()))
db.filterDeliveriesStatusShipped(connection)
