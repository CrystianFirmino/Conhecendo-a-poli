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
                classe TEXT, 
                sugestoes INTEGER, 
                sug_aceitas INTEGER, 
                sug_Naceitas INTEGER
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
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL, 
                descricao TEXT NOT NULL,
                local TEXT,
                data TEXT,
                horario_de_inicio TEXT NOT NULL,
                horario_de_fim TEXT NOT NULL,
                tipo TEXT,  
                aceito INTEGER NOT NULL, 
                autor INTEGER

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
                aceito INTEGER NOT NULL, 
                autor INTEGER

            );
        """
        )

        cursor.execute (

        """
            CREATE TABLE IF NOT EXISTS informacao (
                id INTEGER PRIMARY KEY,
                texto TEXT NOT NULL, 
                aceito INTEGER NOT NULL, 
                autor INTEGER
                );
        """
        )

        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS assuntosXeventos (
                id INTEGER PRIMARY KEY,
                eventoId INTEGER,
                assuntoId INTEGER,
                FOREIGN KEY (eventoId) REFERENCES eventos(id),
                FOREIGN KEY (assuntoId) REFERENCES assuntos(id)
            );
        """
        )
        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS assuntos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
            );
        """
        )

        connection.commit()
        cursor.close()
        connection.close()

    def adicionarInfo(self, texto, user):
        deuCerto = False
        with sqlite3.connect('db1.db') as connection:
            
            cursor = connection.cursor()    
            cursor.execute("""
                            INSERT INTO informacao (texto, aceito)
                            VALUES (?, 0)
                            """, (texto))

            cursor.execute("UPDATE user SET sugestoes = sugestoes + 1 WHERE id = 1")

            connection.commit()
            deuCerto = True
        return deuCerto

    def adicionarLocal(self, nome, bloco, sala, descricao):
        deuCerto = False
        with sqlite3.connect('db1.db') as connection:
            
            cursor = connection.cursor()    
            cursor.execute("""
                            INSERT INTO local(nome, bloco, sala, descricao, aceito)
                            VALUES (?, ?, ?, ?, 0)
                            """, (nome, bloco, sala, descricao))

            cursor.execute("UPDATE user SET sugestoes = sugestoes + 1 WHERE id = 1")
            
            connection.commit()
            deuCerto = True
        return deuCerto

    def adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim, tipo, assunto):
        """
        Assunto deve ser uma lista com nome(s) do(s) assunto(s) do evento
        """
        
        deuCerto = False
        with sqlite3.connect('db1.db') as connection:
            
            cursor = connection.cursor()    
            cursor.execute("""
                            INSERT INTO eventos(nome, descricao, local, data, horario_de_inicio, horario_de_fim, tipo, aceito)
                            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                            """, (nome, descricao, local, data, horarioIn, horarioFim, tipo))
            
            id_ev = cursor.execute("SELECT id FROM eventos WHERE descricao = ? AND local = ?", (descricao, local))
            
            for a in assunto:

                id_ass = cursor.execute("SELECT id FROM assuntos WHERE nome = ?", a)
                cursor.execute("INSERT INTO assuntosXenventos VALUES (?, ?)", (id_ev, id_ass))


            cursor.execute("UPDATE user SET sugestoes = sugestoes + 1 WHERE id = 1")

            connection.commit()
            deuCerto = True
        return deuCerto

    def listarInfos(self):

        with sqlite3.connect('db1.db') as connection:

            cursor = connection.cursor()

            lista = ("SELECT * FROM informacao WHERE aceito = 1")
            result = cursor.execute(lista).fetchall()

        return result

    def listarLocais(self):

        with sqlite3.connect('db1.db') as connection:

            cursor = connection.cursor()

            lista = ("SELECT * FROM local WHERE aceito = 1")
            result = cursor.execute(lista).fetchall()
            
        return result
      
    def listarEventos(self, data, dataFim, horarioIn="00", horarioFim="24", tipo=False, assunto=False):    
        """
        Assunto deve ser uma lista com nome(s) do(s) assunto(s) do evento
        """
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
            filtro1 = cursor.execute(lista, (data, dataFim, horarioIn, horarioFim)).fetchall()
            
            filtro2 = []
            if not assunto == False:
        
                for a in assunto:
                    ids = cursor.connect("SELECT id FROM assuntos WHERE nome =  ", a)
                    #ids dos eventos q cumprem os requisitos de assunto 
                    filtro2 = cursor.execute("SELECT eventoId FROM assuntosXeventos WHERE assuntoId = ?", ids)
                    
                    for ev in filtro1:
                        if ev in filtro2:
                            result.append(ev)
            else:
                for i in filtro1:
                    result.append(cursor.execute("SELECT * FROM evetos WHERE id = ?", i))
            
        #remove duplicatas
        result = list(dict.fromkeys(result))

        return result

    def cadastrar_pessoa(self,user, senha, email, classe = "usuario"):
        try:
            with sqlite3.connect('db1.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO user(usuario, email, senha, classe, sugestoes, sug_aceitas, sug_Naceitas ) VALUES(?, ?, ?, ?, 0, 0, 0)', (user, email, senha, classe))
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

    def listarGrade(self, user):
        """
        Input: id do user.
        Output: lista com nome, data, hora_inicio e hora_fim para cada evento da grade do usuario.
        """
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()

            eventos = cursor.execute("SELECT eventoId FROM eventos WHERE userId = ?", user).fetchall
            result = []
            for evento in eventos:
                result.append = cursor.execute("""SELECT nome, data, horario_de_inicio, horario_de_fim 
                                                    FROM eventos WHERE id = ?""", evento)
        return result 

    def listaNAceitos(self):
        """
        Retorna uma lista de 3 tuplas. 1 = lista de eventos, 2 = lista de locais, 3 = lista de informaçoes
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

            aceitos = []
            recusados = []
            
            form1 = "UPDATE ? SET aceito = 1 WHERE id = ?"
            form2 = "DELETE FROM ? WHERE id = ?"
            form3 = "SELECT autor FROM ? WHERE id = ?" 

            for evento in lista_eve:
                
                tabela  = "eventos"

                if lista_eve[evento] == 's':
                    
                    cursor.execute(form1, (tabela, evento))
                    #add id do autor da sugestao
                    aceitos.append(cursor.execute(form3, (tabela, evento))) 

                if lista_eve[evento] == 'n':
                    
                    cursor.execute(form2, (tabela, evento))
                    recusados.append(cursor.execute(form3, (tabela, evento)))
            
            for local in lista_loc:

                tabela = "local"

                if lista_loc[local] == 's':

                    cursor.execute(form1, (tabela, local))
                    aceitos.append(cursor.execute(form3, (tabela, local)))
                    
                if lista_loc[local] == 'n':

                    cursor.execute(form2, (tabela, local))
                    recusados.append(cursor.execute(form3, (tabela, local)))

            for info in lista_info:

                tabela = "informacao"

                if lista_info[info] == 's':

                    cursor.execute(form1, (tabela, info))
                    aceitos.append(cursor.execute(form3, (tabela, info)))
                
                if lista_info[info] == 'n':

                    cursor.execute(form2, (tabela, info))
                    recusados.append(cursor.execute(form3, (tabela, info)))
                
        for user_id in aceitos:
            cursor.execute("UPDATE user SET sug_aceitas = sug_aceitas + 1 WHERE id = ?", user_id)

        for user_id in recusados:
            cursor.execute("UPDATE user SET sug_Naceitas = sug_Naceitas + 1 WHERE id = ?", user_id)

    def gerenciarColab(self, user):
        """
        Input: id do user que vai ser promovido
        """
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE user
                SET calsse = "coordenador"
                WHERE id = ?
                """, (user))

            


banco = Banco()





