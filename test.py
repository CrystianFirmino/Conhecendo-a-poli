import sqlite3


from db_create import Banco

b = Banco()

assunto = ['Eletrica', 'Civil', 'Computacao']
tipo = False
result = []
user = 3
with sqlite3.connect('db1.db') as connection:
    cursor = connection.cursor()
    # # cursor.execute("""INSERT INTO grade (userId, segunda, terca, quarta, quinta, sexta, sabado) 
    # #                             VALUES (?, '', '', '', '', '', '')""", (user,))
    
    # tbl = cursor.execute("SELECT segunda, terca, quarta, quinta, sexta, sabado FROM grade WHERE userId = ?", (user,)).fetchall()
    # print(tbl)
    # connection.commit()

    semat = [('rber, rveertv, , vert, erver, ,', ' , cwec, wcew, , , , ', 'rber, rveertv, , vert, erver, ,', ' , cwec, wcew, , , , ''rber, rveertv, , vert, erver, ,', ' , cwec, wcew, , , , ')]

    semat = list(semat[0])

    for i in range(len(semat)):
        semat[i] = semat[i].split(",")
    print(semat)
        
