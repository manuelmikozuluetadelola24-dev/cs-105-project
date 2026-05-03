
import PySide6.QtSql

config = open("config", "r")
db_name = config.readline()
db_name = db_name.strip()
db_host = config.readline()
db_host = db_host.strip()
db_user = config.readline()
db_user = db_user.strip()
db_pass = config.readline()
db_pass = db_user.strip()

config.close()

app_db = PySide6.QtSql.QSqlDatabase.addDatabase("QMYSQL")
app_db.setDatabaseName(db_name)
app_db.setHostName(db_host)
app_db.setUserName(db_user)
app_db.setPassword(db_pass)

print(app_db.connectionName())
