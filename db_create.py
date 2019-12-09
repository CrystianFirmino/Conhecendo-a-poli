# -*- coding: utf-8 -*-
import sqlite3
import mysql.connector
from mysql.connector import errorcode

class Banco():
    def criarTabelas(self):

        connection = sqlite3.connect('db1.db')
        

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor = connection.cursor()

        cursor.execute (

        """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                classe TEXT
                );
        """
        )
        
        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL, 
                descricao TEXT NOT NULL,
                local TEXT,
                data TEXT,
                horario_de_inicio TEXT NOT NULL,
                horario_de_fim TEXT NOT NULL,
                tipo TEXT, 
                assunto TEXT, 
                aceito INTEGER NOT NULL

            );
        """
        )

        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS grade (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                eventoId INTEGER,
                FOREIGN KEY (userId) REFERENCES user(id),
                FOREIGN KEY (eventoId) REFERENCES evento(id)
            );
        """
        )
        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS local (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL, 
                bloco TEXT NOT NULL,
                sala TEXT,
                descricao TEXT NOT NULL

            );
        """
        )

        connection.commit()
        cursor.close()
        connection.close()

    def adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim, tipo, assunto):
        deuCerto = False
        with sqlite3.connect('db1.db') as connection:
            
            cursor = connection.cursor()    
            cursor.execute("""
                            INSERT INTO eventos(nome, descricao, local, data, horario_de_inicio, horario_de_fim, tipo, assunto, aceito)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (nome, descricao, local, data, horarioIn, horarioFim, tipo, assunto, 0)
                           )
            connection.commit()
            deuCerto = True
        return deuCerto

    def listarEventos(self, data, horarioIn, horarioFim):    
        
        with sqlite3.connect('db1.db') as connection:

            cursor = connection.cursor()
            result = cursor.execute("""
                                    SELECT * FROM eventos
                                    WHERE data >= ? AND horario_de_inicio >= ? AND horario_de_fim <= ?
                                    """ , (data, horarioIn, horarioFim)).fetchall()
        return result

    def listarEventos2(self, data, dataFim, horarioIn="00", horarioFim="24", tipo=False, assunto=False):    
        
        with sqlite3.connect('db1.db') as connection:

            cursor = connection.cursor()

            lista = ("""SELECT * FROM eventos WHERE aceito = 1 
            AND data >= ? 
            AND data <= ? 
            AND horario_de_inicio >= ? 
            AND horario_de_fim <= ?
            """)
            
            if not tipo == False:
                lista = lista + "AND tipo = " + str(tipo)
            if not assunto == False:
                lista = lista + "AND assunto = " + str(assunto)
            
            result = cursor.execute(lista, (data, dataFim, horarioIn, horarioFim)).fetchall()
        return result

    def cadastrar_pessoa(self,user, senha, email, classe = "usuario"):
        try:
            with sqlite3.connect('db1.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO user(usuario, email, senha, classe) VALUES(?, ?, ?, ?)', (user, email, senha, classe))
                connection.commit()
                return True
        except:
            return False
   
    def buscar_pessoa(self, usr, senha):
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()
            find_user = ("SELECT * FROM user WHERE usuario = ? AND senha = ?")
            results = cursor.execute(find_user, (usr, senha)).fetchall()
        return results

    def colocarNaGrade(self, usr, evento):
        try:
            with sqlite3.connect('db1.db') as connection:
                cursor = connection.cursor()
                
                find_userId = ("SELECT id FROM user WHERE usuario = ?")
                cursor.execute(find_userId, (usr,))
                result0 = cursor.fetchall()
                
                x= result0[0]
                find_eventoId = ("SELECT id FROM eventos WHERE nome = ?")
                cursor.execute(find_eventoId, (evento,))
                result1 = cursor.fetchall()
                y = result1[0]
                x = x + y
                set_grade = ("INSERT INTO grade userId = ?, eventoId = ?")
                cursor.execute(set_grade,x)
                connection.commit()
                print(x)
            return True
        except:
            print("deu ruim")
            return False    

    def listaNAceitos(self, tipo):
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor() 
            
            if tipo == "eventos":    
                results = cursor.execute("SELECT * FROM eventos WHERE aceito = 0").fetchall() 

            elif tipo == "local":
                results = cursor.execute("SELECT * FROM eventos WHERE aceito = 0").fetchall()
    
            return results

    def aceitarCoisasTest(self, lista_s, lista_n):
        """
        Atualiza as listas de eventos e locais. lista_s e lista_n são listas de listas de forma (tipo de tópico, número de aceitos/ n aceitos).
        linha0: eventos, linha1: local.
        """
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()

            for j in range(len(lista_s)):

                if j == 0:
                    tabela = "eventos"
                if j == 1:
                    tabela = "local"

                for i in range(len(lista_s[j])):
                    cursor.execute(
                    """
                    UPDATE ?
                    SET aceito = 1
                    WHERE id = ?
                    """, (tabela, lista_s[j][i]))
            
            for j in range(len(lista_n)):

                if j == 0:
                    tabela = "eventos"
                if j == 1:
                    tabela = "local"

                for i in range(len(lista_n[j])):
                    cursor.execute(
                    """
                    UPDATE ?
                    SET aceito = 1
                    WHERE id = ?
                    """, (tabela, lista_n[j][i]))

            


banco = Banco()
#adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim)
#banco.adicionarEvento("Maratona de Programação","CCP: código, café e pizza","No NCE","04/11", "09", "14", "computação", "vacas, vacathon")
#banco.adicionarEvento("PESC","Apresentações sobre tudo que tem de bom: de jogos à IA","No Bloco H","04/11", "09", "14", "seminários", "IA, jogos, xexeo")
#banco.adicionarEvento("SENEL","tá achando que a gente só faz bomba? Então venha nos ver explodir alguma coisa!","No Bloco A","04/11", "09", "14", "apresentações","bombas")
#banco.adicionarEvento("INSCREVA-SE NA MINERVABOTS","Gosta de robôs? e competições TOPS com todo o Brasil","No Face","04/11", "09", "14","inscrição, competição","robótica")
#resultado = banco.listarEventos("04/11", "09", "14")
#banco.adicionarEvento("Festa de mascara", 'vai ser bom', 'reitoria', '8/10', '18', '00', 'festa', 'todos' )
print(banco.listaNAceitos("eventos"))
lt_s = [[1, 2, 3, 4], []]
lt_n = [[],[]]
#banco.aceitarCoisasTest(lt_s, lt_n)


#print(resultado)
