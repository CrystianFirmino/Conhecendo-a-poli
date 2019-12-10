from flask import session

class Pessoa:
    def __init__(self):
        self.__classe = "none"
        self.iniciar(0, 0, 0, 0)

    def iniciar(self, id, nome, senha, email):
        self.priority = 0
        self._id = id
        self._nome = nome
        self._email = email
        self._senha=senha
        self.valido = self.validar()
    
    def validar(self):
        self.set_priority()
        session['priority'] = self.priority
        if self.priority == 0:
            session['logged_in'] = False
            session['user'] = ""
            session['user_id'] = ""
        elif self.priority>0:
            session['logged_in'] = True
            session['user'] = self._nome
            session['user_id'] = int(self._id)
        #Para (futuramente) verificar se a pessoa é valida
        valido = True
        return valido

    def get_classe(self):
        return self.__classe
    
    def set_priority(self):
        self.priority = 0
        if self.get_classe() == "usuario":
            self.priority = 2
        if self.get_classe() == "coordenador":
            self.priority = 4
        if self.get_classe() == "adm":
            self.priority = 5

    def get_nome(self):
        return self._nome

    def alterar_senha(self):
        return "Ainda nao e possivel alterar a senha"
        
class Usuario(Pessoa):
    def __init__(self, id, nome, senha, email):
        self.__classe = "usuario"
        self.iniciar(id, nome, senha, email)
 
    def get_classe(self):
        return self.__classe

class Coordenador(Pessoa):
    def __init__(self, id, nome, senha, email):
        self.__classe = "coordenador"
        self.iniciar(id, nome, senha, email)
 
    def get_classe(self):
        return self.__classe

class Adm(Coordenador):
    def __init__(self, id, nome, senha, email):
        self.__classe = "adm"
        self.iniciar(id, nome, senha, email)
 
    def get_classe(self):
        return self.__classe

