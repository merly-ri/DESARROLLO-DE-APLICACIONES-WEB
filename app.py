from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = form.usuario.data
        password = form.password.data

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, usuario, password FROM usuarios WHERE usuario = %s",
            (usuario,)
        )

        datos = cursor.fetchone()

        cursor.close()
        conn.close()

        if datos and check_password_hash(datos[2], password):
            usuario_obj = Usuario(
                datos[0],
                datos[1],
                datos[2]
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
        cursor = conn.cursor()

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

        flash(
            "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
            "success"
        )

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

    return render_template(
        "index.html",
        informacion=informacion
    )


# =========================
# PRODUCTOS
# =========================

@app.route("/productos")
@login_required
def productos():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id
        """
    )

    datos = cursor.fetchall()

    productos = []

    for producto in datos:
        productos.append({
            "id": producto[0],
            "nombre": producto[1],
            "categoria": producto[2],
            "precio": producto[3],
            "stock": producto[4]
        })

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos,
        titulo="Productos"
    )


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (nombre, categoria, precio, stock)
            VALUES (%s, %s, %s, %s)
            """,
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


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        WHERE id = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos"))

    form = ProductoForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s
            WHERE id = %s
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Producto actualizado correctamente.", "success")

        return redirect(url_for("productos"))

    if not form.is_submitted():
        form.nombre.data = producto[1]
        form.categoria.data = producto[2] or ""
        form.precio.data = producto[3]
        form.stock.data = producto[4] if producto[4] is not None else 0

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Editar producto"
    )


@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for("productos"))


# =========================
# CLIENTES
# =========================

@app.route("/clientes")
@login_required
def clientes():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre, correo, telefono
        FROM clientes
        ORDER BY id
        """
    )

    datos = cursor.fetchall()

    clientes = []

    for cliente in datos:
        clientes.append({
            "id": cliente[0],
            "nombre": cliente[1],
            "correo": cliente[2],
            "telefono": cliente[3]
        })

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes,
        titulo="Clientes"
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO clientes
            (nombre, correo, telefono)
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Cliente guardado correctamente.", "success")

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Nuevo cliente"
    )


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre, correo, telefono
        FROM clientes
        WHERE id = %s
        """,
        (id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if not cliente:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("clientes"))

    form = ClienteForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE clientes
            SET nombre = %s,
                correo = %s,
                telefono = %s
            WHERE id = %s
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Cliente actualizado correctamente.", "success")

        return redirect(url_for("clientes"))

    if not form.is_submitted():
        form.nombre.data = cliente[1]
        form.correo.data = cliente[2]
        form.telefono.data = cliente[3]

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Editar cliente"
    )


@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM clientes WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes"))


# =========================
# PROVEEDORES
# =========================

@app.route("/proveedores")
@login_required
def proveedores():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre, telefono, email, contacto, productos, estado
        FROM proveedores
        ORDER BY id
        """
    )

    datos = cursor.fetchall()

    proveedores = []

    for proveedor in datos:
        proveedores.append({
            "id": proveedor[0],
            "nombre": proveedor[1],
            "telefono": proveedor[2],
            "correo": proveedor[3],
            "contacto": proveedor[4],
            "productos": proveedor[5],
            "estado": proveedor[6]
        })

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        titulo="Proveedores"
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores
            (nombre, telefono, email, contacto, productos, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.contacto.data,
                form.correo.data,
                form.contacto.data,
                form.productos.data,
                form.estado.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Proveedor guardado correctamente.", "success")

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Nuevo proveedor"
    )


@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre, telefono, email, contacto, productos, estado
        FROM proveedores
        WHERE id = %s
        """,
        (id,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if not proveedor:
        flash("Proveedor no encontrado.", "danger")
        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE proveedores
            SET nombre = %s,
                telefono = %s,
                email = %s,
                contacto = %s,
                productos = %s,
                estado = %s
            WHERE id = %s
            """,
            (
                form.nombre.data,
                form.contacto.data,
                form.correo.data,
                form.contacto.data,
                form.productos.data,
                form.estado.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Proveedor actualizado correctamente.", "success")

        return redirect(url_for("proveedores"))

    if not form.is_submitted():
        form.nombre.data = proveedor[1]
        form.contacto.data = proveedor[4] or proveedor[2]
        form.correo.data = proveedor[3]
        form.productos.data = proveedor[5]
        form.estado.data = proveedor[6]

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Editar proveedor"
    )


@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM proveedores WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Proveedor eliminado correctamente.", "success")

    return redirect(url_for("proveedores"))


# =========================
# FACTURACIÓN
# =========================

@app.route("/facturacion")
@login_required
def facturacion():
    facturas_lista = [
        {
            "numero": "F001-001",
            "cliente": "Lorena López",
            "fecha": "16/08/2026",
            "total": 25.50,
            "estado": "Pagada"
        },
        {
            "numero": "F001-002",
            "cliente": "Paul Pérez",
            "fecha": "16/08/2026",
            "total": 40.00,
            "estado": "Pendiente"
        },
        {
            "numero": "F001-003",
            "cliente": "Laura Torres",
            "fecha": "16/08/2026",
            "total": 18.75,
            "estado": "Pagada"
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas_lista,
        titulo="Facturación"
    )


if __name__ == "__main__":
    app.run(debug=True)