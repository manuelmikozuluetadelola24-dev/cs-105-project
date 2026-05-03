import db

connection = db.initializeConnection(*(db.getConfig()))
db.listDeliveries(connection)
