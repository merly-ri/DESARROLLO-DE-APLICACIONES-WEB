import mysql.connector
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mer2007",
        database="sistema_web"
    )