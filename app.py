from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from forms.facturacion_form import FacturacionForm

from conexion import obtener_conexion
from models import Usuario, obtener_usuario_por_id


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-ponycenter"

csrf = CSRFProtect(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


# =========================
# LOGIN
# =========================

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


# =========================
# REGISTRO
# =========================

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


# =========================
# LOGOUT
# =========================

@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash("Sesión cerrada correctamente.", "info")

    return redirect(url_for("login"))


# =========================
# INICIO
# =========================

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

def cargar_opciones_facturacion(form):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nombre
        FROM clientes
        ORDER BY nombre
        """
    )

    clientes = cursor.fetchall()

    form.cliente_id.choices = [
        (cliente[0], cliente[1])
        for cliente in clientes
    ]

    cursor.execute(
        """
        SELECT id, nombre
        FROM productos
        ORDER BY nombre
        """
    )

    productos = cursor.fetchall()

    form.producto_id.choices = [
        (producto[0], producto[1])
        for producto in productos
    ]

    cursor.close()
    conn.close()


@app.route("/facturacion")
@login_required
def facturacion():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            f.id,
            f.numero,
            c.nombre,
            p.nombre,
            f.fecha,
            f.cantidad,
            f.total,
            f.estado
        FROM facturas f
        INNER JOIN clientes c
            ON f.cliente_id = c.id
        INNER JOIN productos p
            ON f.producto_id = p.id
        ORDER BY f.id
        """
    )

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    facturas = []

    for factura in datos:
        facturas.append({
            "id": factura[0],
            "numero": factura[1],
            "cliente": factura[2],
            "producto": factura[3],
            "fecha": factura[4],
            "cantidad": factura[5],
            "total": factura[6],
            "estado": factura[7]
        })

    return render_template(
        "facturacion.html",
        facturas=facturas,
        titulo="Facturación"
    )


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_facturacion():
    form = FacturacionForm()

    cargar_opciones_facturacion(form)

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO facturas
            (
                numero,
                cliente_id,
                producto_id,
                fecha,
                cantidad,
                total,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                form.numero.data,
                form.cliente_id.data,
                form.producto_id.data,
                form.fecha.data,
                form.cantidad.data,
                form.total.data,
                form.estado.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Factura registrada correctamente.", "success")

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Nueva factura"
    )


@app.route("/facturacion/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_facturacion(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            numero,
            cliente_id,
            producto_id,
            fecha,
            cantidad,
            total,
            estado
        FROM facturas
        WHERE id = %s
        """,
        (id,)
    )

    factura = cursor.fetchone()

    cursor.close()
    conn.close()

    if not factura:
        flash("Factura no encontrada.", "danger")
        return redirect(url_for("facturacion"))

    form = FacturacionForm()

    cargar_opciones_facturacion(form)

    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE facturas
            SET
                numero = %s,
                cliente_id = %s,
                producto_id = %s,
                fecha = %s,
                cantidad = %s,
                total = %s,
                estado = %s
            WHERE id = %s
            """,
            (
                form.numero.data,
                form.cliente_id.data,
                form.producto_id.data,
                form.fecha.data,
                form.cantidad.data,
                form.total.data,
                form.estado.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Factura actualizada correctamente.", "success")

        return redirect(url_for("facturacion"))

    if not form.is_submitted():
        form.numero.data = factura[1]
        form.cliente_id.data = factura[2]
        form.producto_id.data = factura[3]
        form.fecha.data = factura[4]
        form.cantidad.data = factura[5]
        form.total.data = factura[6]
        form.estado.data = factura[7]

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Editar factura"
    )


@app.route("/facturacion/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_facturacion(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM facturas WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Factura eliminada correctamente.", "success")

    return redirect(url_for("facturacion"))


if __name__ == "__main__":
    app.run(debug=True)