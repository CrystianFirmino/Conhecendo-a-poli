from flask import Flask, request, render_template, redirect, url_for, session
import os
from db_create import Banco
from pessoas import Pessoa, Usuario, Coordenador, Adm

app = Flask(__name__)

#print(exemplo_usr.get_classe())

@app.route("/")
def inicio():
    banco = Banco()
    return render_template('inicio.html', eventos = banco.listarEventos("0000", "9999"))

@app.route("/sugerir", methods = ['POST'])
def sugerir():
    nome = str(request.form["nome"])
    descricao = str(request.form["descricao"])
    local = str(request.form["local"])
    dataIn = str(request.form["data_inicio"])
    horarioIn = str(request.form["hora_inicio"])
    horarioFim = str(request.form["hora_fim"])
    try:
        tipo = str(request.form["tipo"])
    except:
        tipo = ''
    assunto = []
    try:
        assunto.append(str(request.form["assunto1"]).title())
        assunto.append(str(request.form["assunto2"]).title())
    except:
        print("Nem todos assuntos selecionados -> /sugerir")

    banco = Banco()
    banco.adicionarEvento(nome, descricao, local, dataIn, horarioIn, horarioFim, tipo, assunto, session['user_id'])
    
    return render_template('sugerir_topicos.html', teste = ["Enviado"])

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
    if len(busca) > 0:    
        x = busca[0]
        id = x[0]
        usuario = x[1]
        email = x[2]
        classe = x[4]

        session['logged_in'] = True
        if classe == "usuario":
            visitante = Usuario(id, usuario, senha, email)
        elif classe == "coordenador":
            visitante = Coordenador(id, usuario, senha, email)
        elif classe == "adm":
            visitante = Adm(id, usuario, senha, email)
        else:
            print("Um erro com as classes -> /logar")
            session['logged_in'] = False
    
    visitante.validar()
    try:
        if session['logged_in']:
            return redirect('/')
        else:
            return render_template('login.html', erro_log = True)
    except:
        return "Concerte isso"

@app.route("/sair")
def sair():
    session['logged_in'] = False
    session['user'] = ""
    session['user_id'] = ""
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
    if (banco.buscar_pessoa(usr, senha) == []):
        cadastrado =  banco.cadastrar_pessoa(usr, senha, email)
    else:
        return 'usuário já existente'
    if cadastrado:
        return redirect('/')
    else:
        return render_template('cadastro.html', erro_cad = True)

@app.route("/encontrar_atividades")
def encontrar_atividades():
    banco = Banco()
    return render_template('encontrar_atividades.html', eventos = banco.listarEventos("04/11", "30/12","05","22"))

@app.route("/grade")
def grade():
    try:
        x = session['grade']
    except:
        session['grade'] = []
        for j in range(2,8):
            session['grade'].append("")
            session['grade'][j-2] = []
            for i in range(7, 20):
                session['grade'][j-2].append("")

    return render_template('grade.html')

@app.route("/enviar_grade", methods = ['POST'])
def enviar_grade():
    grade=[]
    for j in range(2,8):
        grade.append("")
        grade[j-2]=[]
        for i in range(7, 20):
            stg = str(j) + "_" + str(i)
            try:
                app = request.form[stg]
                grade[j-2].append(app.strip())
            except:
                grade[j-2].append("")
    session['grade'] = grade

    return redirect('/grade')

@app.route("/sugerir_topicos")
def sugerir_topicos():
    return render_template('sugerir_topicos.html')

@app.route("/aceitar_topicos")
def aceitar_topicos():
    banco = Banco()
    return render_template('aceitar_topicos.html', eventos = banco.listarNAceitos()[0])

@app.route("/topico_aceito", methods = ['POST'])
def topico_aceito():

    try:
        eventos = {request.form["eventos"]:'s'}
    except:
        eventos = {}
    try:
        informacoes = {request.form["informacoes"]:'s'}
    except:
        informacoes = {}
    try:
        locais = {request.form["locais"]:'s'}
    except:
        locais = {}
    banco = Banco()
    banco.aceitarCoisas(eventos, locais, informacoes)
    return redirect('/aceitar_topicos')

@app.route("/topico_recusado", methods = ['POST'])
def topico_recusado():

    try:
        eventos = {request.form["eventos"]:'n'}
    except:
        eventos = {}
    try:
        informacoes = {request.form["informacoes"]:'n'}
    except:
        informacoes = {}
    try:
        locais = {request.form["locais"]:'n'}
    except:
        locais = {}
    banco = Banco()
    banco.aceitarCoisas(eventos, locais, informacoes)
    return redirect('/aceitar_topicos')

@app.route("/gerenciar_colaboradores")
def gerenciar_colaboradores():
    return render_template('gerenciar_colaboradores.html')

@app.route("/seja_colaborador")
def seja_colaborador():
    return render_template('formulario_colaborador.html')
@app.route("/colaborar", methods = ['POST'])
def calaborar():
    nome = str(request.form["nome_colab"]).title()
    curso = str(request.form["curso"]).title()
    ano = str(request.form["ano"]).title()
    obs = str(request.form["obs"])

    print("Seja um colaborador: ")
    print("Nome: ", nome, "| Curso: ", curso, "| Ano: ", ano, "| Obs: ", obs, "| Id: ", session['user_id'])
    return redirect('/seja_colaborador')

app.secret_key = os.urandom(12)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)