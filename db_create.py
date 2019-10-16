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
                horario_de_fim TEXT NOT NULL

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

    def adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim, tipo, assunto):

        with sqlite3.connect('db1.db') as connection:
            
            cursor = connection.cursor()    
            cursor.execute("""
                            INSERT INTO eventos(nome, descricao, local, data, horario_de_inicio, horario_de_fim, tipo, assunto)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (nome, descricao, local, data, horarioIn, horarioFim, tipo, assunto)
                           )
            connection.commit()

    def listarEventos(self, data, horarioIn, horarioFim):    
        
        with sqlite3.connect('db1.db') as connectio:

            cursor = connectio.cursor()
            result = cursor.execute("""
                                    SELECT nome, descricao, local FROM eventos
                                    WHERE data = ? AND horario_de_inicio > ? AND horario_de_fim < ?
                                    """ , (data, horarioIn, horarioFim)).fetchall()
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
            cursor.execute(find_user, (usr, senha))
            results = cursor.fetchall()
        return results

    def aceitarEvento(self, usr, evento):
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
                print(x)
                a= 1
                b= 2
                set_grade = ("INSERT INTO grade userId = ?, eventoId = ?")
                cursor.execute(set_grade,(a, b,))
                connection.commit()
            return True
        except:
            print("deu ruim")
            return False    

banco = Banco()
#adicionarEvento(self, nome, descricao, local, data, horarioIn, horarioFim)
#banco.adicionarEvento("Maratona de Programação","CCP: código, café e pizza","No NCE","04/11", "09", "14", "computação", "vacas, vacathon")
#banco.adicionarEvento("PESC","Apresentações sobre tudo que tem de bom: de jogos à IA","No Bloco H","04/11", "09", "14", "seminários", "IA, jogos, xexeo")
#banco.adicionarEvento("SENEL","tá achando que a gente só faz bomba? Então venha nos ver explodir alguma coisa!","No Bloco A","04/11", "09", "14", "apresentações","bombas")
#banco.adicionarEvento("INSCREVA-SE NA MINERVABOTS","Gosta de robôs? e competições TOPS com todo o Brasil","No Face","04/11", "09", "14","inscrição, competição","robótica")
resultado = banco.listarEventos("04/11", "09", "14")
print(resultado)
