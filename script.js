const formulario = document.getElementById("formServicio");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("listaServicios");
const contador = document.getElementById("contador");

let total = 0;

formulario.addEventListener("submit", function(e) {
    e.preventDefault();

    if (nombre.value.trim() === "" || descripcion.value.trim() === "" || categoria.value === "") {
        mensaje.innerHTML = '<div class="alert alert-danger">Complete todos los campos.</div>';
        return;
    }

    mensaje.innerHTML = '<div class="alert alert-success">Servicio registrado correctamente.</div>';

    const tarjeta = document.createElement("div");
    tarjeta.className = "card shadow p-3 mt-3";

    const titulo = document.createElement("h5");
    titulo.textContent = nombre.value;

    const texto = document.createElement("p");
    texto.textContent = descripcion.value;

    const tipo = document.createElement("p");
    tipo.innerHTML = "<strong>Categoría:</strong> " + categoria.value;

    const boton = document.createElement("button");
    boton.textContent = "Eliminar";
    boton.className = "btn btn-danger btn-sm";

    boton.addEventListener("click", function() {
        lista.removeChild(tarjeta);
        total--;
        contador.textContent = total;
    });

    tarjeta.appendChild(titulo);
    tarjeta.appendChild(texto);
    tarjeta.appendChild(tipo);
    tarjeta.appendChild(boton);

    lista.appendChild(tarjeta);

    total++;
    contador.textContent = total;

    formulario.reset();
});