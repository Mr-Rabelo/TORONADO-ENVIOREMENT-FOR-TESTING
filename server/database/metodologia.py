import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import metodologia

TABLE = "TEFT.metodologia"

def creat_metodologia(metodologia):
    comando = """INSERT INTO {} (objetivo, N_pessoas, subgrupo, procedimento, N_voltas) VALUE(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(TABLE, metodologia.objetivo, metodologia.N_pessoas, metodologia.subgrupo, metodologia.procedimento, metodologia.N_voltas)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None

def apagar(metodologia):
    comando = """DELETE FROM {} WHERE id_metodologia = \'{}\'""".format(TABLE, metodologia.id_metodologia)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None
