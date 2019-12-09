# -*- coding: utf-8 -*-
import sqlite3
import mysql.connector
from mysql.connector import errorcode

class Banco():
    def criarTabelas(self):

        connection = sqlite3.connect('db1.db')
        

        # if connection.is_connected():
        #     db_Info = connection.get_server_info()
        #     print("Connected to MySQL Server version ", db_Info)
        #     cursor = connection.cursor()
        #     cursor.execute("select database();")
        #     record = cursor.fetchone()
        #     print("You're connected to database: ", record)
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
                descricao TEXT NOT NULL, 
                aceito INTEGER NOT NULL

            );
        """
        )

        cursor.execute (

        """
            CREATE TABLE IF NOT EXISTS informacao (
                id INTEGER PRIMARY KEY,
                texto TEXT NOT NULL, 
                aceito INTEGER NOT NULL
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

    def listaNAceitos(self):
        """
        Retorna uma lista de 3 listas. 1 = lista de eventos, 2 = lista de locais, 3 = lista de informaçoes
        (tablas de locais e informacoes ainda n tem conluna aceito)
        """
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor() 
            
            res_eventos = cursor.execute("SELECT * FROM eventos WHERE aceito = 0").fetchall() 
            res_local = cursor.execute("SELECT * FROM local WHERE aceito = 0").fetchall()
            res_informacao = cursor.execute("SELECT * FROM informacao WHERE aceito = 0").fetchall()
            
            results = []
            results.append(res_eventos)
            results.append(res_local)
            results.append(res_informacao)
            return results

    def aceitarCoisas(self, lista_eve, lista_loc, lista_info):
        """
        Atualiza as tabelas de eventos, locais e info. 
        Cada uma das lista do input deve ser um dicionário com o ID e o resultado da sugestao(s ou n)
        """
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()


            for evento in lista_eve:
                if lista_eve[evento] == 's':

                    cursor.execute(
                        """
                        UPDATE eventos
                        SET aceito = 1
                        WHERE id = ?
                        """, (evento))
                
                if lista_eve[evento] == 'n':
                    cursor.execute(
                        """
                        DELETE FROM eventos
                        WHERE id = ?
                        """, (evento))
            
            for local in lista_loc:
                if lista_loc[local] == 's':

                    cursor.execute(
                        """
                        UPDATE local
                        SET aceito = 1
                        WHERE id = ?
                        """, (local))
                
                if lista_loc[local] == 'n':
                    cursor.execute(
                        """
                        DELETE FROM local
                        WHERE id = ?
                        """, (local))

            for info in lista_info:
                if lista_info[info] == 's':

                    cursor.execute(
                        """
                        UPDATE informacao
                        SET aceito = 1
                        WHERE id = ?
                        """, (info))
                
                if lista_info[info] == 'n':
                    cursor.execute(
                        """
                        DELETE FROM informacao
                        WHERE id = ?
                        """, (info))
                
                    

            


banco = Banco()
#adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim)
#banco.adicionarEvento("Maratona de Programação","CCP: código, café e pizza","No NCE","04/11", "09", "14", "computação", "vacas, vacathon")
#banco.adicionarEvento("PESC","Apresentações sobre tudo que tem de bom: de jogos à IA","No Bloco H","04/11", "09", "14", "seminários", "IA, jogos, xexeo")
#banco.adicionarEvento("SENEL","tá achando que a gente só faz bomba? Então venha nos ver explodir alguma coisa!","No Bloco A","04/11", "09", "14", "apresentações","bombas")
#banco.adicionarEvento("INSCREVA-SE NA MINERVABOTS","Gosta de robôs? e competições TOPS com todo o Brasil","No Face","04/11", "09", "14","inscrição, competição","robótica")
#resultado = banco.listarEventos("04/11", "09", "14")
#banco.adicionarEvento("Festa de mascara", 'vai ser bom', 'reitoria', '8/10', '18', '00', 'festa', 'todos' )

banco.criarTabelas()
print(banco.listaNAceitos())

lt_s = [[1, 2, 3, 4], []]
lt_n = [[],[]]
#banco.aceitarCoisasTest(lt_s, lt_n)


#print(resultado)
