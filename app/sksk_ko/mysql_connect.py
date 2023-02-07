import mysql.connector


cnx = mysql.connector.connect(
    user = 'sksk_ko',
    password = 'Ka83hH36',
    host = 'localhost',
    port = '23306'
)

cursor = cnx.cursor(dictionary=True)
cursor.execute('SELECT * FROM sksk_ko.user')

for row in cursor.fetchall():
    print(row)