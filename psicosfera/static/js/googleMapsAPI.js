var apiKey = '{{ settings.GOOGLE_MAPS_API_KEY }}';
// Función para cargar la API de Google Maps
function cargarAPI() {
    var script = document.createElement('script');
    script.src = 'https://maps.googleapis.com/maps/api/js?key=' + apiKey + '&libraries=places';
    script.defer = true;
    script.async = true;

    script.onload = function () {
        // API de Google Maps cargada, puedes utilizarla aquí
    };

    document.head.appendChild(script);
}