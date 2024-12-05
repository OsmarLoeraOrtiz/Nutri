var nombre_nutriologo;
var especialidad_nutriologo;
var direccion_nutriologo;
var usuario;
function mostrar_contenido() {
    var especialidad = document.getElementById("specialty-input").value;
    var location = document.getElementById("location-input").value;
    var listaDeUbicaciones = [];
    var listaDenutriologos = [];

    $.ajax({
        type: "GET",  // Puedes cambiar el método HTTP según tus necesidades
        url: "filtrar_nutriologos/",  
        data: { especialidad: especialidad },
        success: function(data) {
            if(data.length > 0){
                //Para asegurar que el formato donde se mostrara el mapa y los esp. exista (ya que existe el caso de que no
                //hay coincidencias y modifica el contenedor, se debe crear siempre.)
                var mapContainer = document.querySelector('.contenedor-mapa-contenido');
                mapContainer.innerHTML = '';
                var mapCard = `
                <div class="contenedor-mapa">
                    <div class="divisor-2 mapa">
                        <div id="map" class="divisor-2"></div>
                    </div>
                    <div class="divisor-2" id="zona-especialista">
                        
                    </div>
                </div>
                `;

                // Agregar la tarjeta de usuario al contenedor
                mapContainer.innerHTML += mapCard;

                // Supongamos que userContainer es el elemento contenedor con la clase 'divisor-2'
                var userContainer = document.querySelector('#zona-especialista');

                // Limpiar el contenido existente
                userContainer.innerHTML = '';
                

                // Iterar a través de los datos y agregar las tarjetas al contenedor
                for (var i = 0; i < data.length; i++) {
                    var dataString = JSON.stringify(data[i]);
                    // Eliminar comillas y corchetes
                    dataString = dataString.replace(/[\[\]"]+/g, '');
                    var userParts = dataString.split(",");

                    nombre_nutriologo = userParts[0];
                    especialidad_nutriologo = userParts[1];
                    direccion_nutriologo = userParts[2];
                    usuario = userParts[3];
                    foto = userParts[4];
                    costo_consulta = userParts[5];
                    ubicacion = userParts[6];

                    //console.log("Nombre: " + userParts[0]);
                    //console.log('Especialidad: ' + userParts[1]);
                    //console.log('Dirección: ' + userParts[2]);

                    userParts[2] = userParts[2].replace(/-/g, ','); //Direccion del consultorio
                    userParts[6] = userParts[6].replace(/-/g, ','); //Ubicacion del nutriologo
                    listaDeUbicaciones.push(userParts[2]);
                    listaDenutriologos.push(userParts[0] + "," + userParts[1]);

                    agregarnutriologo(userParts[2],location);

                    console.log('validacion: ' + consultorioCercaDelRango);
                    if (consultorioCercaDelRango == true){
                        var userCard = `
                        <a href="../perfil/${userParts[3]}">
                            <div class="card card-small">
                                <div class="card-body profile-card pt-4 d-flex flex-column align-items-center">
                                    <img src="data:image/jpeg;base64,${userParts[4]}" alt="Profile" class="carta_perfil">
                                    <br>
                                    <h2>${userParts[0]}</h2>
                                    <h3>${userParts[1]}</h3>
                                    <h5>${userParts[6]}</h5>
                                    <h5>$${userParts[5]} </h5>
                                </div>
                            </div>
                        </a>
                    `;

                    // Agregar la tarjeta de usuario al contenedor
                    userContainer.innerHTML += userCard;
                    } 
                }
                var noCard = `
                <div class="titulo-terapia">
                    <h5>No se encontraron Especialistas en un rango de 10 km.</h5>
                </div>
                `;
                if (userContainer == ''){
                    userContainer.innerHTML += noCard;
                }
            }
            else{
                var userContainer = document.querySelector('.contenedor-mapa-contenido');
                // Limpiar el contenido existente
                userContainer.innerHTML = '';
                var userCard = `
                    <div class="titulo-terapia">
                        <h5>No se encontraron coincidencias. Verifica tus datos e intentalo de nuevo.</h5>
                    </div>
                    `;

                    // Agregar la tarjeta de usuario al contenedor
                    userContainer.innerHTML += userCard;
            }

            //Se ejecuta la funcionalidad de buscar en el mapa
            buscar(listaDeUbicaciones,listaDenutriologos);
        },
        error: function(xhr, status, error) {
            // Manejar errores aquí
            console.error("Error en la solicitud AJAX:", error);
        }
    });
}

var consultorioCercaDelRango = true ;
function agregarnutriologo(coordenadas,location) {
    actualizarCoordenadasInput(location)
        .then(function (coordenadasActualizadas) {
            console.log("Ubicación que se transforma a coordenadas:", coordenadasActualizadas);
            console.log("ubicacion que se transforma a coordenadas: " + coordenadas);
            var geocoder = new google.maps.Geocoder();
            // Utiliza la API de Google Maps Geocoding para obtener las coordenadas de la ubicación
            geocoder.geocode({ 'address': coordenadas }, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var lat = results[0].geometry.location.lat();
                    var lng = results[0].geometry.location.lng();

                    // Almacena las coordenadas en la variable coordConsultorio
                    var coordConsultorio = { lat: lat, lng: lng };
                    console.log('coordenadas: ' + coordConsultorio.lat + "," + coordConsultorio.lng);

                    console.log('coordConsultorio: '+ coordConsultorio);
                    console.log('coordenadasINPUT: '+ coordenadasActualizadas);
                    // Comprobación si la coordenada está dentro del rango de 1000 metros
                    var distancia = calcularDistancia(coordConsultorio, coordenadasActualizadas);
                    if (distancia <= 10000) {
                        console.log('La ubicación está dentro del rango: ' + coordenadas);
                        consultorioCercaDelRango = true;
                        console.log('El consultorio esta cerca del rango: ' + consultorioCercaDelRango);
                        console.log('Distancia en metros: ' + distancia);
                    } else {
                        console.log('La ubicación está fuera del rango: ' + coordenadas);
                        consultorioCercaDelRango = false
                        console.log('El consultorio esta cerca del rango: ' + consultorioCercaDelRango);
                        console.log('Distancia en metros: ' + distancia);
                    }
                } else {
                    // Maneja el error de geocodificación aquí
                    console.error('Error al obtener coordenadas para la ubicación:', coordenadas);
                }
            });
        })
        .catch(function (error) {
                // Manejar el error si la actualización de coordenadas falla
                console.error('Error al actualizar coordenadas:', error);
            });
}



// Función para calcular la distancia entre dos coordenadas en metros
function calcularDistancia(coord1, coord2) {
    var R = 6371000; // Radio de la Tierra en metros
    var lat1 = toRadians(coord1.lat);
    var lon1 = toRadians(coord1.lng);
    var lat2 = toRadians(coord2.lat);
    var lon2 = toRadians(coord2.lng);

    var dLat = lat2 - lat1;
    var dLon = lon2 - lon1;

    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1) * Math.cos(lat2) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);

    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    var distance = R * c; // Distancia en metros
    console.log("Coordenadas consultorio antes: " +coord1.lat + "," + coord1.lng);
    console.log("Coordenadas ubicacion antes: " +coord2.lat + "," + coord2.lng);
    console.log("Distancia antes: " + distance);
    return distance;
    
}

// Función para convertir grados a radianes
function toRadians(degrees) {
    return degrees * Math.PI / 180;
}

function actualizarCoordenadasInput(location) {
    return new Promise((resolve, reject) => {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({ 'address': location }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var lat = results[0].geometry.location.lat();
                var lng = results[0].geometry.location.lng();
                // Actualiza las coordenadas en la variable coordenadasINPUT
                var coordenadas = { lat: lat, lng: lng };
                console.log("-----Coordenadas ubicacion antes DE llmar-----: " + coordenadas.lat + "," + coordenadas.lng);
                resolve(coordenadas);
            } else {
                // Maneja el error de geocodificación aquí
                console.error('Error al obtener coordenadas para la ubicación:', location);
                reject('Error al obtener coordenadas');
            }
        });
    });
}

