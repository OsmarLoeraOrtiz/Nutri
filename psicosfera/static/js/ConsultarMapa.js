var coordenadasINPUT = {};

function buscar(listaDeUbicaciones,listaDePsicologos) {
    var location = document.getElementById("location-input").value;
    const mapElement = document.getElementById('map');
    var radio = 10000; // Radio en metros (10 kilómetros)

    // Utiliza la API de Google Maps Geocoding para obtener las coordenadas de la ubicación
    var geocoder = new google.maps.Geocoder();

    geocoder.geocode({ 'address': location }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var lat = results[0].geometry.location.lat();
            var lng = results[0].geometry.location.lng();

            // Almacena las coordenadas en la variable coordenadas
            coordenadasINPUT = { lat: lat, lng: lng };


            //console.log('Coordenadas:', coordenadasINPUT.lat, coordenadasINPUT.lng);

            var map = new google.maps.Map(mapElement, {
                zoom: 14,
                center: coordenadasINPUT
            });
            var marker = new google.maps.Marker({
                position: coordenadasINPUT,
                map: map
            });

            // Crea un círculo que representa el rango de distancia
            var circle = new google.maps.Circle({
                strokeColor: '#6CAEDC',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#6CAEDC',
                fillOpacity: 0.35,
                map: map,
                center: coordenadasINPUT,
                radius: radio  // Radio en metros
            });

            colocarMarcasEnUbicaciones(map, listaDeUbicaciones, listaDePsicologos); //Esta función hace que se pongan las marcas de los psicologos que aparecen

            // Cambiar estilo del segundo div para hacerlo visible
            document.querySelector(".contenedor-mapa").style.display = "flex";

            
        
        } else {
            // Maneja el error de geocodificación aquí
            alert('Ingrese una ubicación correcta.');
        }
    });
}


function colocarMarcasEnUbicaciones(map, ubicaciones, info_psicologo) {
    var geocoder = new google.maps.Geocoder();

    for (var i = 0; i < ubicaciones.length; i++) {
        // Utiliza una función de cierre (closure) para mantener el contexto de cada iteración
        (function(index) {
            var location = ubicaciones[index];
            var info = info_psicologo[index];

            geocoder.geocode({ 'address': location }, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var lat = results[0].geometry.location.lat();
                    var lng = results[0].geometry.location.lng();

                    var coordConsultorio = { lat: lat, lng: lng };

                    /*var marker = new google.maps.Marker({
                        position: coordConsultorio,
                        map: map,
                        title: location,
                        icon: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                        visible: false // Hacer que el marcador sea invisible
                    });*/

                    var circle = new google.maps.Circle({
                        strokeColor: '#FF69B4', // Rosa claro en formato hexadecimal
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillColor: '#FF69B4', // Rosa claro en formato hexadecimal
                        fillOpacity: 0.35,
                        map: map,
                        center: coordConsultorio,
                        radius: 500  // Radio en metros
                    });                    

                    var partesInfo = info.split(',');

                    // Crear el contenido HTML con estilos para la ventana de información
                    var contentHTML = '<div class="cartaIcono_nombre">' + partesInfo[0] + '</div>' +
                                    '<div class="especialidad">' + partesInfo[1] + '</div>';


                    var infoWindow = new google.maps.InfoWindow({
                        content: contentHTML
                    });

                   // Asociar el InfoWindow con el evento de mouseover del círculo
                    google.maps.event.addListener(circle, 'mouseover', function(event) {
                        infoWindow.setPosition(event.latLng); // Establecer la posición del InfoWindow en el punto donde el mouse entró al círculo
                        infoWindow.open(map);
                    });

                    // Asociar el InfoWindow con el evento de mouseout del círculo
                    google.maps.event.addListener(circle, 'mouseout', function() {
                        infoWindow.close();
                    });
                } else {
                    console.error('Error al obtener coordenadas para la ubicación:', location);
                }
            });
        })(i);
    }
}
