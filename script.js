const formulario=document.getElementById("formServicio");
const nombre=document.getElementById("nombre");
const descripcion=document.getElementById("descripcion");
const categoria=document.getElementById("categoria");
const mensaje=document.getElementById("mensaje");
const lista=document.getElementById("listaServicios");
const contador=document.getElementById("contador");
const spinner=document.getElementById("spinnerCarga");

let servicios=[
{
nombre:"Diseño Web",
descripcion:"Creación de páginas web modernas y responsivas.",
categoria:"Diseño Web"
},
{
nombre:"Desarrollo Web",
descripcion:"Aplicaciones web funcionales y dinámicas.",
categoria:"Desarrollo Web"
},
{
nombre:"Mantenimiento",
descripcion:"Actualización y soporte de sitios web.",
categoria:"Mantenimiento"
}
];

nombre.addEventListener("input",function(){
if(nombre.value.trim().length<3){
nombre.classList.add("is-invalid");
nombre.classList.remove("is-valid");
}else{
nombre.classList.add("is-valid");
nombre.classList.remove("is-invalid");
}
});

descripcion.addEventListener("input",function(){
if(descripcion.value.trim().length<10){
descripcion.classList.add("is-invalid");
descripcion.classList.remove("is-valid");
}else{
descripcion.classList.add("is-valid");
descripcion.classList.remove("is-invalid");
}
});

categoria.addEventListener("change",function(){
if(categoria.value===""){
categoria.classList.add("is-invalid");
categoria.classList.remove("is-valid");
}else{
categoria.classList.add("is-valid");
categoria.classList.remove("is-invalid");
}
});

function mostrarServicios(){

lista.innerHTML="";

if(servicios.length===0){
lista.innerHTML='<div class="col-12"><div class="alert alert-warning mt-3">No existen servicios registrados.</div></div>';
contador.textContent=0;
return;
}

servicios.forEach(function(servicio,index){

const tarjeta=document.createElement("div");
tarjeta.className="col-md-4 mb-4";

tarjeta.innerHTML=`
<div class="card shadow h-100">
<div class="card-body">
<h5 class="card-title">${servicio.nombre}</h5>
<p class="card-text">${servicio.descripcion}</p>
<p><strong>Categoría:</strong> ${servicio.categoria}</p>
<button class="btn btn-danger btn-sm">Eliminar</button>
</div>
</div>
`;

tarjeta.querySelector("button").addEventListener("click",function(){
servicios.splice(index,1);
mostrarServicios();
});

lista.appendChild(tarjeta);

});

contador.textContent=servicios.length;

}

formulario.addEventListener("submit",function(e){

e.preventDefault();

if(nombre.value.trim()===""||descripcion.value.trim()===""||categoria.value===""){
mensaje.innerHTML='<div class="alert alert-danger">Complete todos los campos.</div>';
return;
}

if(nombre.value.trim().length<3||descripcion.value.trim().length<10||categoria.value===""){
mensaje.innerHTML='<div class="alert alert-danger">Corrija los errores antes de registrar.</div>';
return;
}

spinner.classList.remove("d-none");

setTimeout(function(){

servicios.push({
nombre:nombre.value,
descripcion:descripcion.value,
categoria:categoria.value
});

mostrarServicios();

mensaje.innerHTML='<div class="alert alert-success">Servicio registrado correctamente.</div>';

spinner.classList.add("d-none");

const modal=new bootstrap.Modal(document.getElementById("modalRegistro"));
modal.show();

formulario.reset();

nombre.classList.remove("is-valid","is-invalid");
descripcion.classList.remove("is-valid","is-invalid");
categoria.classList.remove("is-valid","is-invalid");

},1000);

});

mostrarServicios();