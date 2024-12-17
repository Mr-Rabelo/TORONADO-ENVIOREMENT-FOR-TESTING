import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import circuito

TABLE = "TEFT.circuito"

def creat_circuito(circuito):
    comando = """INSERT INTO {} (nome, tempo_descolcamento, KM, curvas, cones, local) VALUE(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(TABLE, circuito.nome, circuito.tempo_descolcamento, circuito.KM, circuito.curvas, circuito.cones, circuito.local)
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
    