import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import membros
TABLE = "TEFT.membro"

def login(email, senha):
    comando = ("SELECT * FROM {} WHERE email = '{}' and senha = '{}'".format(TABLE, email, senha)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linha = cursor.fetchall()
            # verifica a informação 
            if len(linha) == 0:
                var_login = False
            else:
                var_login = True
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_membros():
    comando = ("SELECT * FROM {} ".format(TABLE)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(membros.Membros(linha[1], None, linha[0], linha[2]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def creat_membro(membro):
    pass