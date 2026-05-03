import pymysql.cursors

connection = pymysql.connect(host="192.168.122.105", user="app", password="app_pass", database="test")

with connection:
	with connection.cursor() as cursor:
		sql_statement = "INSERT INTO `Tests` (`test_id`, `test_name`) VALUES (%s, %s)"
		cursor.execute(sql_statement, ("32", "test_guy"))

	connection.commit()

	with connection.cursor() as cursor:
		
		sql = "SELECT `test_id`, `test_name` FROM `Tests`"
		cursor.execute(sql)
		result = cursor.fetchone()
		print(result)
