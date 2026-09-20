from flask_login import UserMixin
from conexion import obtener_conexion

class Usuario(UserMixin):
    def __init__(self, id, usuario, password):
        self.id = id
        self.usuario = usuario
        self.password = password

def obtener_usuario_por_id(id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, usuario, password FROM usuarios WHERE id = %s",
        (id,)
    )
    datos = cursor.fetchone()
    cursor.close()
    conn.close()

    if datos:
        return Usuario(datos["id"], datos["usuario"], datos["password"])

    return None