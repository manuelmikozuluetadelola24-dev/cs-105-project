import pymysql.cursors

# NOTE: Every function that executes a mysql query will close the connection passed
#    to them once they finish executing.

# NOTE: order_by parameters must be passed a string containing a column name
#    enclosed in backticks: "`colname`" or "`tblname`.`colname`"

# NOTE: order parameters must be passed the following strings: "DESC" or "ASC"

# NOTE: filter functions usually expect a string containing an SQL string enclosed
#    in single quotes: "'filter_string'"

def outputQueryToConsole(sql, result):
    print("Query: " + sql + "\n")
    for row in result:
        print(row)

# MySQL Server Connection
config = []

def getConfig():
    global config
    config_file = open("config", "r")
    for line in config_file:
        config.append(line.strip())
    
    config.append("")
    config.append("")
    config_file.close()

def initializeConnection():
    global config
    db_host, db_name, db_user, db_pass = config
    connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name, cursorclass=pymysql.cursors.Cursor)
    return connection

def checkUser(db_user, db_pass):
    db_host = config[0]
    db_name = config[1]
    is_login_correct = False
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
        is_login_correct
        is_login_correct = True
        connection.close()
    except pymysql.err.OperationalError:
        is_login_correct = False

    return is_login_correct

# Delivery Tracking

def listDeliveries(connection, order="DESC", order_by="`DELIVERY`.`delivery_id`"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `DELIVERY`.`delivery_id`, `customer_name`, `ORDERS`.`order_id`, `delivery_date`, `DELIVERY`.`status`, `delivered_by`, CONCAT(`delivery_street`, ' ', `delivery_barangay`, ' ', `delivery_city`) AS `delivery_address` FROM `DELIVERY` JOIN `ORDERS` ON `DELIVERY`.`order_id` = `ORDERS`.`order_id` JOIN `CUSTOMER` ON `CUSTOMER`.`customer_id` = `CUSTOMER`.`customer_id` ORDER BY " + order_by + " " + order
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

def filterDeliveriesBy(connection, status="'DELIVERED'"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `DELIVERY`.`delivery_id`, `customer_name`, `delivery_date`, `DELIVERY`.`status`, `delivered_by` FROM `DELIVERY` JOIN `ORDERS` ON `DELIVERY`.`order_id` = `ORDERS`.`order_id` JOIN `CUSTOMER` ON `ORDERS`.`customer_id` = `CUSTOMER`.`customer_id` WHERE `DELIVERY`.`status` = " + status
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

# General Utility

def filterProductByCategory(connection, category):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `PRODUCT`.`product_id`, `product_name`, `price`, `stock_quantity` FROM `PRODUCT` JOIN `PRODUCT_CATEGORY` ON `PRODUCT`.`category_id` = `PRODUCT_CATEGORY`.`category_id` WHERE `PRODUCT_CATEGORY`.`category_name` = " + category
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

def listCustomers(connection, order="DESC", order_by="`customer_name`"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `customer_id`, `customer_name`, `customer_city`, `contact_number` FROM `CUSTOMER` ORDER BY " + order_by + " " + order
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

# Inventory Management

def listStockLevel(connection, order="ASC", order_by="`stock_quantity`"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `PRODUCT`.`product_id`, `product_name`, `category_name`, `stock_quantity`, `price` FROM `PRODUCT` JOIN `PRODUCT_CATEGORY` ON `PRODUCT`.`category_id` = `PRODUCT_CATEGORY`.`category_id` ORDER BY " + order_by + " " + order
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

def addShipmentItemToProductStockLevel(connection):
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `PRODUCT` JOIN `SHIPMENT_ITEM` ON `PRODUCT`.`product_id` = `SHIPMENT_ITEM`.`product_id` JOIN `SHIPMENT` ON `SHIPMENT_ITEM`.`shipment_id` = `SHIPMENT`.`shipment_id` SET `PRODUCT`.`stock_quantity` = `PRODUCT`.`stock_quantity` + `SHIPMENT_ITEM`.`quantity` WHERE `SHIPMENT`.`status` = 'DELIVERED'"
            cursor.execute(sql)

def listLowStockLevel(connection, low_threshold="10"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `PRODUCT`.`product_id`, `product_name`, `PRODUCT_CATEGORY`.`category_name`, `stock_quantity` FROM `PRODUCT` JOIN `PRODUCT_CATEGORY` ON `PRODUCT`.`category_id` = `PRODUCT_CATEGORY`.`category_id` WHERE `PRODUCT`.`stock_quantity` <= " + low_threshold + " ORDER BY `PRODUCT`.`stock_quantity` ASC"
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

# Order Handling

def listOrderWithCustomerInfo(connection, order="DESC", order_by="`order_date`"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `ORDERS`.`order_id`, `customer_name`, `order_date`, `order_type`, `ORDERS`.`status`, `total_price` FROM `ORDERS` JOIN `CUSTOMER` ON `ORDERS`.`customer_id` = `CUSTOMER`.`customer_id` ORDER BY " + order_by + " " + order
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

def listOrderItemsInOrder(connection, with_id, order="DESC", order_by="`order_id`"):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `ORDER_ITEM`.`order_item_id`, `product_name`, `ORDER_ITEM`.`quantity`, `selling_price`, (`ORDER_ITEM`.`quantity` * `selling_price`) AS `item_total` FROM `ORDER_ITEM` JOIN `PRODUCT` ON `ORDER_ITEM`.`product_id` = `PRODUCT`.`product_id` WHERE `ORDER_ITEM`.`order_id`= " + with_id + "  ORDER BY " + order_by + " " + order
            cursor.execute(sql)
            result = cursor.fetchall()
            outputQueryToConsole(sql, result)
            return result

def deductFromStock(connection, deduct_amount, with_id):
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `PRODUCT` SET `stock_quantity` = `stock_quantity` " + deduct_amount + " WHERE `PRODUCT`.`product_id` = " + with_id
            cursor.execute(sql)

# new_status values: "'PENDING'", "'SHIPPED'", "'DELIVERED'", "'CANCELLED'"
def updateOrderStatus(connection, new_status, with_id):
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `ORDERS` SET `ORDERS`.`status` = " + new_status + " WHERE `ORDERS`.`order_id` = " + with_id
            cursor.execute(sql)

# Reporting
