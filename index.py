import mysql.connector;

db_filmes = mysql.connector.connect(
    host='localhost',
    user='root',
    password='LAIS123456',
    database='db_filmes'
)

cursor = db_filmes.cursor()

#todos os usuarios
cursor.execute("SELECT * FROM users")

result = cursor.fetchall()

for i in result:
    print(i)

#print(result)