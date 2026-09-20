import mysql.connector
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Merlyriv0702",
        database="sistema_web"
    )