import  mysql.connector
 

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="abdou5626",
    database="commande_db"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM tactures")

results = cursor.fetchall()


for row in results:
    print(row)

cursor.close()
conn.close()