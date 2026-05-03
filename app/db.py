import pymysql.cursors

# NOTE: Every function that executes a mysql query will close the connection passed
#	to them once they finish executing.

# NOTE: order_by parameters must be passed a string containing a column name
#	enclosed in backticks: "`colname`" or "`tblname`.`colname`"

# NOTE: order parameters must be passed the following strings: "DESC" or "ASC"

# NOTE: filter functions usually expect a string containing an SQL string enclosed
#	in single quotes: "'filter_string'"



# MySQL Server Connection

def getConfig():
	config = []
	config_file = open("config", "r")
	for line in config_file:
		config.append(line.strip())
	
	config_file.close()
	return config

def initializeConnection(*config):
	db_host, db_user, db_pass, db_name = config
	connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name, cursorclass=pymysql.cursors.Cursor)
	return connection

# Delivery Tracking

def listDeliveries(connection, order="DESC", order_by="`DELIVERY`.`delivery_id`"):
	with connection:
		with connection.cursor() as cursor:
			sql = "SELECT `DELIVERY`.`delivery_id`, `customer_name`, `ORDERS`.`order_id`, `delivery_date`, `DELIVERY`.`status`, `delivered_by`, CONCAT(`delivery_street`, ' ', `delivery_barangay`, ' ', `delivery_city`) AS `delivery_address` FROM `DELIVERY` JOIN `ORDERS` ON `DELIVERY`.`order_id` = `ORDERS`.`order_id` JOIN `CUSTOMER` ON `CUSTOMER`.`customer_id` = `CUSTOMER`.`customer_id` ORDER BY " + order_by + " " + order
			print("Query: " + sql + "\n")
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				print(row)

def filterDeliveriesBy(connection, status="'DELIVERED'"):
	with connection:
		with connection.cursor() as cursor:
			sql = "SELECT `DELIVERY`.`delivery_id`, `customer_name`, `delivery_date`, `DELIVERY`.`status`, `delivered_by` FROM `DELIVERY` JOIN `ORDERS` ON `DELIVERY`.`order_id` = `ORDERS`.`order_id` JOIN `CUSTOMER` ON `ORDERS`.`customer_id` = `CUSTOMER`.`customer_id` WHERE `DELIVERY`.`status` = " + status
			print("Query: " + sql + "\n")
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				print(row)

# General Utility

def filterProductByCategory(connection, category):
	with connection:
		with connection.cursor() as cursor:
			sql = "SELECT `PRODUCT`.`product_id`, `product_name`, `price`, `stock_quantity` FROM `PRODUCT` JOIN `PRODUCT_CATEGORY` ON `PRODUCT`.`category_id` = `PRODUCT_CATEGORY`.`category_id` WHERE `PRODUCT_CATEGORY`.`category_name` = " + category
			print("Query: " + sql + "\n")
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				print(row)

def listCustomers(connection, order="DESC", order_by="`customer_name`"):
	with connection:
		with connection.cursor() as cursor:
			sql = "SELECT `customer_id`, `customer_name`, `customer_city`, `contact_number` FROM `CUSTOMER` ORDER BY " + order_by + " " + order
			print("Query: " + sql + "\n")
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				print(row)
