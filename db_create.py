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
                )
        """
        )
        
        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL, 
                descricao TEXT NOT NULL,
                local TEXT,
                horario_de_inicio TEXT,
                horario_de_acabar TEXT
                
            )
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

            )
        """
        )
        cursor.execute (
        """
            CREATE TABLE IF NOT EXISTS grade (
                userId INTEGER NOT NULL,
                eventoId INTEGER NOT NULL,
                FOREIGN KEY (userId) REFERENCES user(id),
                FOREIGN KEY (eventoId) REFERENCES eventos(id)
            )
        """
        )        
        #cursor.execute('ALTER TABLE user ADD classe TEXT')

        connection.commit()

    def adicionarEvento(self):
        pass

    def cadastrar_pessoa(self,user, senha, email):
        try:
            with sqlite3.connect('db1.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO user(usuario, email, senha) VALUES(?, ?, ?)', (user, email, senha))
                connection.commit()
                return True
        except:
            return 'deu ruim no cadastro'
   
    def buscar_pessoa(self, usr, senha):
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()
            find_user = ("SELECT * FROM user WHERE usuario = ? AND senha = ?")
            cursor.execute(find_user, (usr, senha))
            results = cursor.fetchall()
        return results

    def aceitarEvento(self):
        pass

    def listarEventos(self):
        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()
            find_evento = ("SELECT * FROM eventos ")
            cursor.execute(find_evento)
            results = cursor.fetchall()
        return results



banco = Banco()

#banco.cadastrar_pessoa('teste','senha', 'teste@email')
banco.criarTabelas()

resultado = banco.listarEventos()

print(resultado)