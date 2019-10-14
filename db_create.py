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

        with sqlite3.connect('db1.db') as connection:
            cursor = connection.cursor()    
        
            ex = (
            """
                INSERT INTO eventos(nome, descricao, local, data, horario_de_inicio, horario_de_fim) 
                    VALUES (?, ?, ?, ?, ?, ?);       
            """
            )
            cursor.execute("""
                            INSERT INTO eventos(nome, descricao, local, data, horario_de_inicio, horario_de_fim)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (nome, descricao, local, data, horarioIn, horarioFim)
                           )
            connection.commit()
        
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
        pass


banco = Banco()
#banco.cadastrar_pessoa('teste','senha', 'teste@email')
resultado = banco.buscar_pessoa('teste', 'senha')
print(resultado)
