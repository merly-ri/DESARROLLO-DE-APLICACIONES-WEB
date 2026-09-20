from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms.producto_form import ProductoForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from conexion import obtener_conexion
from models import Usuario, obtener_usuario_por_id

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-ponycenter"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)

clientes_lista = [
    {"id": "001", "nombre": "María Rivera", "correo": "maria@example.com", "telefono": "0957654082"},
    {"id": "002", "nombre": "Juan Lopez", "correo": "juan@example.com", "telefono": "0937197654"},
    {"id": "003", "nombre": "Ana Torres", "correo": "ana@example.com", "telefono": "0975632980"}
]

proveedores_lista = [
    {"nombre": "Distribuidora ABC", "contacto": "0989191430", "correo": "cervicios@abc.com", "productos": "Servicios y materiales tecnológicos.", "estado": "Activo"},
    {"nombre": "Comercial XYZ", "contacto": "0958959682", "correo": "accesorios@xyz.com", "productos": "Equipos y accesorios tecnológicos.", "estado": "Activo"}
]

facturas_lista = [
    {"numero": "F001-001", "cliente": "Lorena López", "fecha": "16/08/2026", "total": 25.50, "estado": "Pagada"},
    {"numero": "F001-002", "cliente": "Paul Pérez", "fecha": "16/08/2026", "total": 40.00, "estado": "Pendiente"},
    {"numero": "F001-003", "cliente": "Laura Torres", "fecha": "16/08/2026", "total": 18.75, "estado": "Pagada"}
]

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = form.usuario.data
        password = form.password.data

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, usuario, password FROM usuarios WHERE usuario = %s",
            (usuario,)
        )
        datos = cursor.fetchone()
        cursor.close()
        conn.close()

        if datos and check_password_hash(datos["password"], password):
            usuario_obj = Usuario(
                datos["id"],
                datos["usuario"],
                datos["password"]
            )
            login_user(usuario_obj)
            flash("Inicio de sesión correcto.", "success")
            return redirect(url_for("inicio"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html", form=form)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    form = UsuarioForm()

    if form.validate_on_submit():
        usuario = form.usuario.data
        password = form.password.data

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (usuario,)
        )
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conn.close()
            flash("El usuario ya existe.", "danger")
            return render_template("registro.html", form=form)

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
            (usuario, password_hash)
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Usuario registrado correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def inicio():
    informacion = {
        "nombre": "Sistema Web",
        "descripcion": "Sistema de Desarrollo de Aplicaciones Web",
        "anio": 2026
    }
    return render_template("index.html", informacion=informacion)

@app.route("/productos")
@login_required
def productos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, nombre, categoria, precio, stock FROM productos ORDER BY id"
    )
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("productos.html", productos=productos, titulo="Productos")

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Producto guardado correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Nuevo producto"
    )

@app.route("/clientes")
@login_required
def clientes():
    return render_template(
        "clientes.html",
        clientes=clientes_lista,
        titulo="Clientes"
    )

@app.route("/proveedores")
@login_required
def proveedores():
    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista,
        titulo="Proveedores"
    )

@app.route("/facturacion")
@login_required
def facturacion():
    return render_template(
        "facturacion.html",
        facturas=facturas_lista,
        titulo="Facturación"
    )

if __name__ == "__main__":
    app.run(debug=True)