import sqlite3
import mysql.connector
from mysql.connector import errorcode

from db_create import Banco

b = Banco()


# with sqlite3.connect('db1.db') as connection:
#     cursor = connection.cursor() 
#     cursor.execute("UPDATE user SET sug_aceitas = sug_aceitas + 1 WHERE id = ?", (3,))
#     cursor.execute("UPDATE eventos SET autor = 3")
e ={}
l = {}
i = {}

for k in range(1, 38):
     e[k] = 's'

print(e)
x = b.aceitarCoisas(e, l, i)



