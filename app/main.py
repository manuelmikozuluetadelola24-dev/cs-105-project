from views.login import LoginView
from views.dashboard import DashboardView
import db.db as db
db.getConfig()

def testQueries():
    connection = db.initializeConnection()
    db.listDeliveries(connection, "DESC", "`delivery_id`")
    print("\n\n")
    connection = db.initializeConnection()
    db.filterDeliveriesBy(connection, "'SHIPPED'")
    connection = db.initializeConnection()
    print("\n\n")
    db.filterProductByCategory(connection, "'Canned Goods'")
    connection = db.initializeConnection()
    print("\n\n")
    db.listCustomers(connection, "ASC", "`customer_id`")
    connection = db.initializeConnection()
    print("\n\n")
    db.listStockLevel(connection)

def main():
    login = LoginView()
    login.mainloop()

    if(login.logged_in):
        dashboard = DashboardView(login.user_role)
        dashboard.mainloop()

main()
