import mysql.connector;

db_filmes = mysql.connector.connect(
    host='localhost',
    user='root',
    password='LAIS123456',
    database='db_filmes'
)

cursor = db_filmes.cursor()

cursor.execute("SELECT * FROM users")

result = cursor.fetchall()

print(result)