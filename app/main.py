from views.login import LoginView
from views.dashboard import DashboardView
import db.db

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
	connection = db.initializeConnection(*(db.getConfig()))
	print("\n\n")
	db.listStockLevel(connection)

def main():
    login = LoginView()
    login.mainloop()

    if login.logged_in_role:
        dashboard = DashboardView(login.logged_in_role)
        dashboard.mainloop()

main()
