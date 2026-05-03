import db

def testQueries():
	connection = db.initializeConnection(*(db.getConfig()))
	db.listDeliveries(connection, "DESC", "`delivery_id`")
	print("\n\n")
	connection = db.initializeConnection(*(db.getConfig()))
	db.filterDeliveriesBy(connection, "'SHIPPED'")
	connection = db.initializeConnection(*(db.getConfig()))
	print("\n\n")
	db.filterProductByCategory(connection, "'Canned Goods'")
	connection = db.initializeConnection(*(db.getConfig()))
	print("\n\n")
	db.listCustomers(connection, "ASC", "`customer_id`")

testQueries()
