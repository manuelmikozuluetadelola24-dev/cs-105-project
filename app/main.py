import db

connection = db.initializeConnection(*(db.getConfig()))
db.filterDeliveriesBy(connection, "DELIVERED")
print("\n\n")
connection = db.initializeConnection(*(db.getConfig()))
db.filterDeliveriesBy(connection, "SHIPPED")
