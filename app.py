import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-ponycenter"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "ferreteria.db")

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

def get_db_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio REAL NOT NULL,
            stock INTEGER
        )
    """)
    cantidad = conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    if cantidad == 0:
        productos_iniciales = [
            ("Diseño Web", None, 50.00, None),
            ("Desarrollo Web", None, 80.00, None),
            ("Mantenimiento Web", None, 35.00, None)
        ]
        conn.executemany("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)", productos_iniciales)
        conn.commit()
    conn.close()

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
    conn = get_db_connection()
    productos = conn.execute("SELECT id, nombre, categoria, precio, stock FROM productos ORDER BY id").fetchall()
    conn.close()
    return render_template("productos.html", productos=productos, titulo="Productos")

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (form.nombre.data, form.categoria.data, form.precio.data, form.stock.data)
        )
        conn.commit()
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

init_db()

if __name__ == "__main__":
    app.run(debug=True)