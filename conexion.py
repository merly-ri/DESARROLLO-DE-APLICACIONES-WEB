import psycopg2


def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        database="sistema_web",
        user="postgres",
        password="merly2007"
    )