import sqlite3


from db_create import Banco

b = Banco()

assunto = ['Eletrica', 'Civil', 'Computacao']
tipo = False
result = []
with sqlite3.connect('db1.db') as connection:
    cursor = connection.cursor()
    lista = ("""SELECT id FROM eventos WHERE aceito = 1
    AND data >= ? 
    AND data <= ? 
    AND horario_de_inicio >= ? 
    AND horario_de_fim <= ?
    """)
    if not tipo == False:
        lista = lista + "AND tipo = " + str(tipo)
    #ids dos eventos q cumprem requisitos de horario e tipo 
    filtro1 = cursor.execute(lista, ('01/01', '30/12', '00', '99')).fetchall()
    
    for i in range(len(filtro1)):
        filtro1[i] = filtro1[i][0]

    if not assunto == False:
        filtro2 = []
        
        for a in assunto:
            ids = cursor.execute("SELECT id FROM assuntos WHERE nome = ?;", (a,)).fetchall()
            ids = ids[0][0]

            #ids dos eventos q cumprem os requisitos de assunto 
            filtro2 = cursor.execute("SELECT eventoId FROM assuntosXeventos WHERE assuntoId = ?", (ids,)).fetchall()
            
            for i in range(len(filtro2)):
                filtro2[i] = filtro2[i][0]
            
            for ev in filtro1:
                if ev in filtro2:
                    result.append(cursor.execute("SELECT * FROM eventos WHERE id = ?", (ev,)).fetchall()[0])
            
    else:
        for i in filtro1:
            result.append(cursor.execute("SELECT * FROM eventos WHERE id = ?", (i,)).fetchall()[0])
print(range(4))
#remove duplicatas
#print(result)
rep =[]
for i  in range(len(result)):
    
    for e in range(i+1, len(result)):
    
        if result[i][0] == result[e][0]:
            print ("siiiiim")
            rep.append(result[i])
            print (rep)
for i in rep:
    result.remove(i)
    
#remove duplicatas
#result = list(dict.fromkeys(result))
print(result)