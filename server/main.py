import os
import sys

from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
from datetime import date, datetime

from database import membros as bd_membros 
from database import prototipo as bd_prototipo 
from database import circuito as bd_circuito 
import formatter
from error_reporter import report_error
from classes import membros as mem
from classes import prototipo as prot
from classes import circuito as circu

app = Flask(__name__, template_folder='templates')
app.secret_key = "FormulaUFMG"
CAMINHO_UPLOAD = os.path.join()

# rota para o login 
@app.route("/login", methods=["POST", "GET"])
def login() -> None:
    if request.method == "POST": # verifica o tipo de requisição que o sistema fez
        # coleta as informações da pagina 
        email = request.form.get("email") 
        senha = request.form.get("senha") 
        senha = formatter.encode_password(senha) # codifica a senha 
        verificado, var_login = bd_membros.login(email,senha) # realiza uma pesquisa no banco de dados
        # "verificador" indica que a pesquisa no banco de dados foi realizada com sucesso
        # "var_login" indica se o login pode ser realizado
        if verificado == True and var_login == True:
            session["name"] = email
            return redirect("/inicio")
        elif verificado == True and var_login == False:
            flash("Erro na senha ou no email")
            return redirect("/login")
        elif verificado == False:
            flash("Estamos com problemas com integração com o banco de dados, tente mais tarde")
            return("/login")
    else:
        # renderiza a pagina de login
        return render_template("login.html")

# caminho para a tela de inico do sistema    
@app.route("/inicio")
def inicio():
    if not session.get("name"):
        return redirect("/login")
    else:
        return render_template("inicio.html")

@app.route("/sair")
def sair():
    session["name"] = None
    return redirect("/")

@app.route("/membros")
def membros():
    if not session.get("name"):
        return redirect("/login")
    else:
        membros = bd_membros.get_membros()
        return render_template("membros.html", membros)

@app.route("/cria_conta", methods=["POST", "GET"])
def cria_conta():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "Post":
            nome = request.form.get("nome")
            subgrupo = request.form.get("subgrupo")
            email = request.form.get("email")
            senha = request.form.get("senha")
            senha = formatter.encode_password(senha)
            membro = mem.Membros(email, senha, nome, subgrupo)
            verificador, var_membro = creat_membro(membro)
            if verificador == True and var_membro == True:
                session["name"] = email
                return redirect("/inicio")
            elif verificador == True and var_membro == False:
                flash("Erro ao cria a conta")
                return redirect("/inicio")
            elif verificador == False:
                flash("Estamos com problemas com a integração com o banco de dados")
                return redirect("/inicio")
        else:
            return render_template("cadastro_membro.html")

@app.route("/modifica_conta/<email>", methods=["POST", "GET"])
def modifica_conta(email):
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "Post":
            nome = request.form.get("email")
            subgrupo = request.form.get("email")
            email = request.form.get("email")
            senha = request.form.get("email")
            senha = formatter.encode_password(senha)
            membro = bd_membros.get_membro(email)
            membro.modifica(nome, subgrupo, senha)
            verificador, var_membro = bd_membros.modifica(membro)
            if verificador == True and var_membro == True:
                flash("informaçoes atualizadas")
                return redirect("/inicio")
            elif verificador == True and var_membro == False:
                flash("Erro ao atualizar as informações")
                return redirect("/modifica_conta/{}".format(email))
            elif verificador == False:
                flash("Estamos com problemas na integração com o banco de dados")
                return redirect("/inicio")
        else:
            membro = bd_membros.get_membro(email)
            return render_template("modifica_conta.html",membro = membro)

@app.route("/cria_prototipo", methods=["POST", "GET"])
def cria_prototipo():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "Post":
            nome = request.form.get("nome")
            ano_fabricacao = request.form.get("ano_fabricacao")
            temporada = request.form.get("Temporada")
            peso = request.form.get("Peso")
            status = request.form.get("Status")
            prototipo = prot.Prototipo(None, nome, ano_fabricacao, status, peso, temporada)
            verificador, var_prototipo = bd_prototipo.create_prototipo(prototipo)
            if verificador == True and var_prototipo == True:
                return redirect("/inicio")
            elif verificador == True and var_prototipo == False:
                flash("Erro ao cadastrar o prototipo")
                return redirect("/cria_prototipo")
            elif verificador == False:
                flash("Estamos com problemas com a integração com o banco de dados, tente mais tarde")
                return redirect("/inicio")
        else:
            return render_template("cadastro_prototipo.html")

@app.route("/prototipos")
def prototipos():
    if not session.get("name"):
        return redirect("/login")
    else:
        prototipos = bd_prototipo.get_prototipos()
        render_template("prototipos.html", prototipos=prototipos)

@app.route("/modifica/<id_prototipo>", methods=["POST", "GET"])
def modifica_prototipo(id_prototipo):
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "Post":
            nome = request.form.get("nome")
            ano_fabricacao = request.form.get("ano_fabricacao")
            temporada = request.form.get("Temporada")
            peso = request.form.get("Peso")
            status = request.form.get("Status")
            id_prototipo = request.form.get("id_prototipo")
            prototipo = bd_prototipo.get_prototipo(id_prototipo)
            prototipo.modifica(nome, ano_fabricacao, status, peso, temporada)
            verificador, var_prototipo = bd_prototipo.moodifica(prototipo)
            if verificador == True and var_prototipo == True:
                flash("informações atualizadas")
                return redirect("/inicio")
            elif verificador == True and var_prototipo == False:
                flash("erro ao realiza as modificações")
                return redirect("/modifica/{}".format(id_prototipo))
            elif verificador == False:
                flash("Estamos com problemas na integração com o banco de dados, tente mais tarde")
                return redirect("/inicio")
        else:
            prototipo = bd_prototipo.get_prototipo(id_prototipo)
            return render_template("modifica_prototipo.html", prototipo = prototipo)

@app.route("/cadastro_circuito", methods=["POST", "GET"])
def cadastro_circuito():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "Post":
            nome = request.form.get("nome")
            tempo_descolcamento = request.form.get("tempo")
            KM = request.form.get("kms")
            curvas = request.form.get("curvas")
            cones = request.form.get("cones")
            local = request.form.get("local")
            circuito = circu.Circuito(None, nome, tempo_descolcamento, KM, curvas, cones, local)
            verificador, var_circuito = bd_circuito.create_circuito(circuito)
            if verificador == True and var_circuito == True:
                circuito = bd_circuito.get_circuito_id(circuito)
                pista = request.files["circuito"]
                
        else:
            return render_template("cadastro_cicuito.html")