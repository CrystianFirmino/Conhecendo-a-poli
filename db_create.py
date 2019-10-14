import sqlite3

class Banco():
    def criarTabelas(self):
        connection = sqlite3.connect('db1.db')
        cursor = connection.cursor()   
        cursor.execute (

        """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL
                );
        """
        )

        cursor.execute (
        """
            CREATE TABLE eventos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL, 
                descricao TEXT NOT NULL,
                local TEXT,
                data TEXT,
                horario_de_inicio TEXT NOT NULL,
                horario_de_fim TEXT NOT NULL
                
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

    def adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim):

        cnn = sqlite3.connect('db1.db')
        cursor = cnn.cursor()    
     
        ex = (
        """
            INSERT INTO eventos(nome, descricao, local, data, horario_de_inicio, horario_de_fim) 
                VALUES (?, ?, ?, ?, ?, ?);       
        """
        )
        cursor.execute((ex), (nome, descricao, local, data, horarioIn, horarioFim))
        cnn.commit()
        cursor.close()

    def cadastrarPessoa(self):
        x = 1
    def logarPessoa(self):
        x = 1
    def aceitarEvento(self):
        x = 1
    def listarEventos(self):
        x = 1



banco = Banco()



