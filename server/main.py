import os
import sys

from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
from datetime import date, datetime

from database import membros as bd_membros 
import formatter
from error_reporter import report_error
from classes import membros as mem

app = Flask(__name__, template_folder='templates')
app.secret_key = "FormulaUFMG"

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