function mostrarMapa(ubicacion) {
    var location = ubicacion;
    const mapElement = document.getElementById('map1');

    // Utiliza la API de Google Maps Geocoding para obtener las coordenadas de la ubicación
    var geocoder = new google.maps.Geocoder();

    geocoder.geocode({ 'address': location }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var lat = results[0].geometry.location.lat();
            var lng = results[0].geometry.location.lng();

            // Almacena las coordenadas en la variable coordenadas
            var coordenadas = { lat: lat, lng: lng };

            //console.log('Coordenadas:', coordenadas.lat, coordenadas.lng);
            //console.log('Ubi:', location);

            var panorama = new google.maps.StreetViewPanorama(mapElement, {
                position: coordenadas,
                pov: {
                    heading: 0, // Dirección inicial
                    pitch: 0 // Ángulo de inclinación inicial
                },
                zoom: 1 // Nivel de zoom de la vista de panorama
            });
        } else {
            // Maneja el error de geocodificación aquí
            alert('Ingrese una ubicación correcta.');
        }
    });
}
