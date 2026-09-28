from flask_login import UserMixin
from conexion import obtener_conexion


class Usuario(UserMixin):
    def __init__(self, id, usuario, password):
        self.id = id
        self.usuario = usuario
        self.password = password


def obtener_usuario_por_id(user_id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, usuario, password FROM usuarios WHERE id = %s",
        (user_id,)
    )

    datos = cursor.fetchone()

    cursor.close()
    conn.close()

    if datos:
        return Usuario(
            datos[0],
            datos[1],
            datos[2]
        )

    return None