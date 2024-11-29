// Observar cambios en el contenido de la sección
const observer = new MutationObserver(function (mutationsList, observer) {
    const contenedorMapa = document.querySelector('.contenedor-mapa');
    contenedorMapa.classList.add('expandir');
});

observer.observe(document.querySelector('.contenedor-mapa'), { childList: true });

// Ejecutar la función de expansión inicial
expandirContenedor();

// Función para expandir automáticamente la sección
function expandirContenedor() {
    const contenedorMapa = document.querySelector('.contenedor-mapa');
    contenedorMapa.style.maxHeight = "none"; // Ajusta la altura máxima según tus necesidades
}

// Obtén una referencia al botón de búsqueda
const botonBuscar = document.querySelector('.btn-search');

// Agrega un manejador de eventos para el botón de búsqueda
botonBuscar.addEventListener('click', function () {
    // Muestra el contenido del contenedor-mapa-contenido
    const contenedorMapaContenido = document.querySelector('.contenedor-mapa-contenido');
    contenedorMapaContenido.style.display = 'block';
});
