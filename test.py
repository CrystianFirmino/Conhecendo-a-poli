import sqlite3


from db_create import Banco

b = Banco()

assunto = ['Eletrica', 'Civil', 'Computacao']
tipo = False
result = []
user = 3
with sqlite3.connect('db1.db') as connection:
    cursor = connection.cursor()

    cursor.execute("INSERT INTO assuntos (nome) VALUES ('Ambiental'),('Controle e Automação'),('Materiais'),('Petróleo'),('Produção'),('Eletrônica'),('Mecânica'),('Metalúrgica'),('Naval'),('Nuclear'),('Outros')") 
    connection.commit()