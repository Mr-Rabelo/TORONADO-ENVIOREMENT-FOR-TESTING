import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        con = mysql.connector(host='localhost', database='TEFT', user='root', password='italo175933')
        cursor = con.cursor()
        verificador = True
    except:
        verificador = False
        cursor = None
        con = None
    return verificador, cursor, con
