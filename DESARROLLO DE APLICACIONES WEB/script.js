const formulario = document.getElementById("formServicio");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("listaServicios");
const contador = document.getElementById("contador");

let total = 0;

nombre.addEventListener("input", function () {
    if (nombre.value.trim().length < 3) {
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");
    } else {
        nombre.classList.add("is-valid");
        nombre.classList.remove("is-invalid");
    }
});

descripcion.addEventListener("input", function () {
    if (descripcion.value.trim().length < 10) {
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");
    } else {
        descripcion.classList.add("is-valid");
        descripcion.classList.remove("is-invalid");
    }
});

categoria.addEventListener("change", function () {
    if (categoria.value === "") {
        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");
    } else {
        categoria.classList.add("is-valid");
        categoria.classList.remove("is-invalid");
    }
});

formulario.addEventListener("submit", function (e) {
    e.preventDefault();

    if (nombre.value.trim() === "" || descripcion.value.trim() === "" || categoria.value === "") {
        mensaje.innerHTML = '<div class="alert alert-danger">Complete todos los campos.</div>';
        return;
    }

    if (nombre.value.trim().length < 3 || descripcion.value.trim().length < 10 || categoria.value === "") {
        mensaje.innerHTML = '<div class="alert alert-danger">Corrija los errores antes de registrar.</div>';
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

    boton.addEventListener("click", function () {
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

    nombre.classList.remove("is-valid", "is-invalid");
    descripcion.classList.remove("is-valid", "is-invalid");
    categoria.classList.remove("is-valid", "is-invalid");
});