from flask import Flask, request, render_template, redirect, url_for, session
import os
from db_create import Banco

app = Flask(__name__)

class Pessoa:
    def __init__(self):
        self.__classe = "none"
        self.iniciar( 0, 0, 0)

    def iniciar(self, nome, senha, email):
        self.priority = 0
        self._nome = nome
        self._email = email
        self._senha=senha
        self.valido = self.validar()
    
    def validar(self):
        self.set_priority()
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
    def __init__(self, nome, senha, email):
        self.__classe = "usuario"
        self.iniciar(nome, senha, email)
 
    def get_classe(self):
        return self.__classe

class Coordenador(Pessoa):
    def __init__(self, nome, senha, email):
        self.__classe = "coordenador"
        self.iniciar(nome, senha, email)
 
    def get_classe(self):
        return self.__classe

class Adm(Coordenador):
    def __init__(self, nome, senha, email):
        self.__classe = "adm"
        self.iniciar(nome, senha, email)
 
    def get_classe(self):
        return self.__classe



class bBanco:
    def __init__(self):
        pass

    def cadastrar_pessoa(self, usuario, senha, email):
        #Verificar se os dados são validos
        cadastrado = False

        #Se validos:
            #Salvar Usuario senha e email no Banco
            #cadastrado = True
        
        return cadastrado
        
    def buscar_pessoa(self, usr, senha):
        #Buscar pelo usr (usuario ou email) e senha
        
        #Se encontrado
            #return [classe, usuario, email]
        
        #Se não
            #return []     

        return ["usuario","user","email"] #Provisorio

exemplo_usr = Usuario("Chaves", "chaves@.br", "1234")

visitante = Pessoa()

print(exemplo_usr.get_classe())

@app.route("/")
def inicio():
    return render_template('inicio.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logar", methods = ['POST'])
def logar():
    
    usr = str(request.form["usuario"]).title()
    senha = str(request.form["senha"])
    visitante = Pessoa()

    banco = Banco()
    busca =  banco.buscar_pessoa(usr, senha)
    print(busca)
    if len(busca) > 0:    
        classe = "usuario"
        x = busca[0]
        usuario = x[1]
        email = x[2]
        
        session['logged_in'] = True
        if classe == "usuario":
            visitante = Usuario(usuario, senha, email)
        elif classe == "coordenador":
            visitante = Coordenador(usuario, senha, email)
        elif classe == "adm":
            visitante = Adm(usuario, senha, email)
        else:
            print("Um erro com as classes")
            session['logged_in'] = False
    
    visitante.validar() #inutil
    session['priority'] = visitante.priority
    try:
        if session['logged_in']:
            return redirect('/')
        else:
            return "Login Negado"
    except:
        return "Concerte isso"

@app.route("/sair")
def sair():
    session['logged_in'] = False
    return redirect('/')

@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')

@app.route("/cadastrar", methods = ['POST'])
def cadastrar():
    usr = str(request.form["usuario"]).title()
    email = str(request.form["email"]).title()
    senha = str(request.form["senha"])
    
    banco = Banco()
    cadastrado =  banco.cadastrar_pessoa(usr, senha, email)
    print(cadastrado)
    if cadastrado:
        return redirect('/')
    else:
        return "Cadastro Negado"

@app.route("/encontrar_atividades")
def encontrar_atividades():
    return render_template('encontrar_atividades.html')

@app.route("/grade")
def grade():
    return render_template('grade.html')

@app.route("/sugerir_topicos")
def sugerir_topicos():
    return render_template('sugerir_topicos.html')

@app.route("/aceitar_topicos")
def aceitar_topicos():
    return render_template('aceitar_topicos.html')

@app.route("/gerenciar_colaboradores")
def gerenciar_colaboradores():
    return render_template('gerenciar_colaboradores.html')

app.secret_key = os.urandom(12)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)