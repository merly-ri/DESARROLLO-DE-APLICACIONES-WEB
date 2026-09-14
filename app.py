from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from conexion import obtener_conexion

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-ponycenter"

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

@app.route("/")
def inicio():
    informacion = {
        "nombre": "Sistema Web",
        "descripcion": "Sistema de Desarrollo de Aplicaciones Web",
        "anio": 2026
    }
    return render_template("index.html", informacion=informacion)

@app.route("/productos")
def productos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, categoria, precio, stock FROM productos ORDER BY id")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("productos.html", productos=productos, titulo="Productos")

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
            (form.nombre.data, form.categoria.data, form.precio.data, form.stock.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Producto guardado correctamente.", "success")
        return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=form, titulo="Nuevo producto")

@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=clientes_lista, titulo="Clientes")

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html", proveedores=proveedores_lista, titulo="Proveedores")

@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html", facturas=facturas_lista, titulo="Facturación")

if __name__ == "__main__":
    app.run(debug=True)