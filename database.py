import pymysql

hostname = 'localhost'
user = 'root'
password = ''

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS loans_db")
cursor.execute("SHOW DATABASES")

for databases in cursor:
    print(databases)

cursor.close()
db.close()