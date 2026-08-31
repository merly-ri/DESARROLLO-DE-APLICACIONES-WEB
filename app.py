from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-ponycenter"

productos_lista = [
    {"nombre": "Diseño Web", "descripcion": "Diseño y creación de sitios web modernos y responsive.", "precio": 50.00, "estado": "Disponible"},
    {"nombre": "Desarrollo Web", "descripcion": "Desarrollo de aplicaciones web utilizando tecnologías modernas.", "precio": 80.00, "estado": "Disponible"},
    {"nombre": "Mantenimiento Web", "descripcion": "Mantenimiento y actualización de sitios y aplicaciones web.", "precio": 35.00, "estado": "Disponible"}
]

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
    return render_template("productos.html", productos=productos_lista, titulo="Productos")

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