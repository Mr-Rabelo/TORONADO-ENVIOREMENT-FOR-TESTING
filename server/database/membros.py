import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error
from db_connection import connect_to_db, close_connect_to_bd

from error_reporter import send_email

TABLE = "TEFT.membro"

def login(email, senha):
    comando = ("SELECT * FROM {} WHERE email = '{}' and senha = '{}'".format(TABLE, email, senha)) # comando sql 
    verificador, cursor, con = connect_to_db() # coleta as informações para a conexão com o banco 
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
        close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

