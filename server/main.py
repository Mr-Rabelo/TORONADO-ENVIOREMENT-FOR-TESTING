import os
import sys

from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
from datetime import date, datetime

from database import membros as bd_membros 
from database import prototipo as bd_prototipo 
from database import circuito as bd_circuito 
import formatter
import path_manager
import error_reporter
from server.classes import membros as cl_membro
from server.classes import prototipo as cl_prototipo
from server.classes import circuito as cl_circuito

app = Flask(__name__, template_folder="templates")
app.secret_key = "FormulaUFMG"

@app.route("/")
def index():
    return redirect("/login")

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
            error_reporter.incorrect_access(email)
            return redirect("/login")
        elif verificado == False:
            flash("Estamos com problemas com integração com o banco de dados, tente mais tarde")
            error_reporter.incorrect_access(email)
            return redirect("/login")
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
        verificador, membros = bd_membros.get_membros()
        verificador_membro, usuario = bd_membros.get_membro(session.get("name"))
        if verificador == True and verificador_membro == True:
            if usuario[0].subgrupo == "Data Analysis" or usuario[0].subgrupo == "Gestão" or usuario[0].subgrupo == "Capitania":
                subgrupo = True
            else:
                subgrupo = False
            return render_template("membros.html", membros = membros, subgrupo = subgrupo)
        else:
            return redirect("/inicio")

@app.route("/modifica_conta", methods=["POST", "GET"])
def modifica_conta():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            nome = request.form.get("nome")
            subgrupo = request.form.get("subgrupo")
            email = request.form.get("email")
            senha = request.form.get("senha")
            senha_conf = request.form.get("senha_conf")
            if senha != senha_conf:
                return redirect("/membros")
            else:
                senha = formatter.encode_password(senha)
                verificador, membro = bd_membros.get_membro(email)
                if verificador == True:
                    membro[0].modifica(nome, subgrupo, senha)
                    verificador, var_membro = bd_membros.modifica(membro[0])
                    if verificador == True and var_membro == True:
                        flash("informaçoes atualizadas")
                        return redirect("/inicio")
                    elif verificador == True and var_membro == False:
                        flash("Erro ao atualizar as informações")
                        return redirect("/membros")
                    elif verificador == False:
                        flash("Estamos com problemas na integração com o banco de dados")
                        return redirect("/inicio")
                else:
                    return redirect("/inicio")
        else:
            return redirect("/membros")

@app.route("/apagar_membro", methods=["POST", "GET"])
def apagar_membro():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            email = request.form.get("email")
            verificador, membro = bd_membros.get_membro(email)
            if verificador == True:
                verificador, var_membro = bd_membros.apagar(membro[0])
                if verificador == True and var_membro == True:
                    flash("informações apagadas")
                    return redirect("/inicio")
                else:
                    flash("Erro ao apagar o registro")
                    return redirect("/inicio")
            else:
                flash("Erro ao coletar as informações")
                return redirect("/inicio")
        else:
            return redirect("/inicio")

@app.route("/cria_membro", methods=["POST", "GET"])
def cria_membro():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            nome = request.form.get("nome")
            subgrupo = request.form.get("subgrupo")
            email = request.form.get("email")
            senha = request.form.get("senha")
            senha_conf = request.form.get("senha_conf")
            if senha != senha_conf:
                return redirect("/inicio")
            else:
                senha = formatter.encode_password(senha)
                membro = cl_membro.Membros(email, senha, nome, subgrupo)
                verificador, var_membro = bd_membros.creat_membro(membro)
                if verificador == True and var_membro == True:
                    flash("usuario cadastrado")
                    return redirect("/inicio")
                else:
                    flash("erro ao cadastrar um membro")
                    return redirect("/inicio")
        else:
            return redirect("/inicio")

##-------testa ------------
@app.route("/prototipos")
def prototipos():
    if not session.get("name"):
        return redirect("/login")
    else:
        verificador, prototipos = bd_prototipo.get_prototipos()
        verificador_membro, usuario = bd_membros.get_membro(session.get("name"))
        if verificador == True and verificador_membro == True:
            if usuario[0].subgrupo == "Data Analysis" or usuario[0].subgrupo == "Gestão" or usuario[0].subgrupo == "Capitania":
                subgrupo = True
            else:
                subgrupo = False
            render_template("prototipos.html", prototipos=prototipos, subgrupo = subgrupo)
        else:
            return redirect("/inicio")

@app.route("/modifica_prototipo", methods=["POST", "GET"])
def modifica_prototipo():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            id = request.form.get("id")
            nome = request.form.get("nome")
            ano_fabricacao = request.form.get("ano_fabricacao")
            status = request.form.get("status")
            peso = request.form.get("peso")
            temporada = request.form.get("temporada")
            verificador, prototipo = bd_prototipo.get_prototipo(id)
            if verificador == True:
                prototipo[0].modificar(nome, ano_fabricacao, status, peso, temporada)
                verificador, var_prototipo = bd_prototipo.modifica(prototipo[0])
                if verificador == True and var_prototipo == True:
                    flash("informações atualizadas")
                    return redirect("/inicio")
                else:
                    flash("erro ao modificar as informações")
                    return redirect("/inicio")
            else:
                flash("Erro ao coletar as informações do prototipo")
                return redirect("/inicio")
        else:
            return redirect("/inicio")

@app.route("/apagar_prototipo",  methods=["POST", "GET"])
def apagar_prototipo():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            id_prototipo = request.form.get("id_prototipo")
            verificador, prototipo = bd_prototipo.get_prototipo(id_prototipo)
            if verificador == True:
                verificador, var_prototipo = bd_prototipo.apagar(prototipo[0])
                if verificador == True and var_prototipo == True:
                    flash("Informação apagada")
                    return redirect("/inicio")
                else:
                    flash("Erro ao apagar os registros do prototipo")
                    return redirect("/inicio")
            else:
                flash("Erro ao coletas as informações do banco de dados")
                return redirect("/inicio")
        else:
            return redirect("/inicio")

@app.route("/criar_prototipo", methods=["POST", "GET"])
def criar_prototipo():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            nome = request.form.get("nome")
            ano_fabricacao = request.form.get("ano_fabricacao")
            status = request.form.get("status")
            peso = request.form.get("peso")
            temporada = request.form.get("temporada")
            prototipo = cl_prototipo.Prototipo(None, nome,ano_fabricacao, status, peso, temporada)
            verificador, var_prototipo = bd_prototipo.creat_prototipo(prototipo)
            if verificador == True and var_prototipo == True:
                flash("prototipo criado")
                return redirect("/inicio")
            else:
                flash("Erro ao cadadtrar o prototipo")
                return redirect("/inicio")
        else:
            return redirect("/inicio")

@app.route("/circuito")
def circuito():
    if not session.get("name"):
        return redirect("/login")
    else:
        verificador, circuitos = bd_circuito.get_circuitos()
        verificador_membro, usuario = bd_membros.get_membro(session.get("name"))
        if verificador == True and verificador_membro == True:
            if usuario[0].subgrupo == "Data Analysis" or usuario[0].subgrupo == "Gestão" or usuario[0].subgrupo == "Capitania":
                subgrupo = True
            else:
                subgrupo = False
            return render_template("circuitos.html", circuitos = circuitos, subgrupo = subgrupo)
        else:
            return redirect("/inicio")

@app.route("/cria_circuito", methods=["POST", "GET"])
def cria_circuito():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            nome = request.form.get("nome")
            tempo_descolcamento = request.form.get("tempo_descolcamento")
            KM = request.form.get("KM")
            curvas = request.form.get("curvas")
            cones = request.form.get("cones")
            local = request.form.get("local")
            circuito_ent = cl_circuito.Circuito(None,nome,tempo_descolcamento,KM,curvas,cones,local)
            verificador, var_circuito = bd_circuito.creat_circuito(circuito_ent)
            if verificador == True and var_circuito == True:
                arquivo = request.files['circuito']
                verificador, var_circuito = bd_circuito.get_id(circuito_ent)
                if verificador == True:
                    try:
                        savePath = path_manager.join_path(path_manager.get_upload_path(), var_circuito[0].caminho)
                        arquivo.save(savePath)
                        flash("registro de circuito realizando")
                        return redirect("/inicio")
                    except Exception as e:
                        flash("informações do circuito cadastradas, porem problemas ao salvar a imagem")
                        error_reporter.report_error(e)
                        return redirect("/circuito")
                else:
                    flash("Erro ao busca as informações ja cadastradas")
                    return redirect("/circuito")
            else:
                flash("Erro ao criar um registro de circuito")
                return redirect("/circuito")
        else:
            return redirect("/circuito")

@app.route("/modifica_circuito", methods=["POST", "GET"])
def modifica_circuito():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            id_circuito = request.form.get("id_circuito")
            nome = request.form.get("nome")
            tempo_descolcamento = request.form.get("tempo_descolcamento")
            KM = request.form.get("KM")
            curvas = request.form.get("curvas")
            cones = request.form.get("cones")
            local = request.form.get("local")
            verificador, var_circuito = bd_circuito.get_circuito(id_circuito)
            if verificador == True:
                var_circuito[0].modificar(nome, tempo_descolcamento, KM, curvas, cones, local)
                verificador, var_circuito = bd_circuito.modificar(var_circuito[0])
                if verificador == True and var_circuito == True:
                    flash("informações atualizadas")
                else:
                    flash("Erro ao atualizar as informações")
                    return redirect("/circuito")
                arquivo = request.files['circuito']
                try:
                    savePath = path_manager.join_path(path_manager.get_upload_path(), var_circuito[0].caminho)
                    arquivo.save(savePath)
                    flash("registro de circuito realizando")
                    return redirect("/inicio")
                except Exception as e:
                    flash("informações do circuito cadastradas, porem problemas ao salvar a imagem")
                    error_reporter.report_error(e)
                    return redirect("/circuito")
            else:
                flash("Erro ao criar um registro de circuito")
                return redirect("/circuito")
        else:
            return redirect("/circuito")

@app.route("/apaga_circuito", methods=["POST", "GET"])
def apaga_circuito():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            id_circuito = request.form.get("id_circuito")
            verificador, var_circuito = bd_circuito.get_circuito(id_circuito)
            if verificador == True:
                verificador, var_circuito = bd_circuito.apagar(var_circuito[0])
                if verificador == True and var_circuito == True:
                    flash("Registro apagado")
                    return redirect("/inicio")
                else:
                    flash("Erro ao apagar um registro")
                    return redirect("/circuito")
            else:
                flash("Erro ao pegar as informações sobre o circuito")
                return redirect("/circuito")
        else:
            return redirect("/circuito")

if __name__ == "__name__":
    app.run(debug=True)